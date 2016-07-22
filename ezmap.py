# =================================================
# EzMAP
# Version: 1.0
#
# Author: Patrick Czeczko
# Made at: de Koning Lab
# Link: http://lab.jasondk.io
# Github:
#
# Additional documentation can be found on the github page.
# =================================================

__author__ = 'patrickczeczko'
import sys, os

import Scripts.arguments as arguments
import Scripts.configOptions as config
import Scripts.fileManager as fileman
import Scripts.ensureScriptPermissions as ensureScriptPermissions
import Scripts.prinseqPrep as prinseq
import Scripts.bowtie2Prep as bowtie2
import Scripts.samtoolsPrep as samtools
import Scripts.blastprep as blast
import Scripts.emalPrep as emal
import Scripts.finalScript as final

serialSample = False


# Cretaes a txt file of all importnat output files for final report
def outputFileList(files, projdir, projName):
    outputfile = open(projdir + '6-FinalResult-' + projName + '/information/' + 'filelist.txt', 'w+')
    outputfile.write(
        '<table class="table table-striped table-bordered"><thead><tr><td>Filename</td><td>Path</td></tr></thead>')

    outputfile.write('<tbody>')
    for x in files:
        outputfile.write('<tr><td>' + files[x].origFileName + '</td><td>' + files[x].origFilePath.replace('/',
                                                                                                          '&#47;') + '</td></tr>')
    outputfile.write('</tbody></table>')


def runEzMapOnTimePoint(configOptions, startAtStep, inputFileDir, projdir):
    startStep = startAtStep

    print(inputFileDir)
    print(projdir)

    if not inputFileDir.endswith("/"):
        inputFileDir = inputFileDir + '/'

    if not projdir.endswith("/"):
        projdir = projdir + '/'

    # Get list of FASTQ files to process
    origFiles = fileman.getListOfOriginalFiles(inputFileDir, projdir)

    # Check if there is at least one file to process
    if len(origFiles) < 1:
        print('No files found to process!')
        print('Exiting...')
        return

    # Create subdirectories where intermediate files will live
    createdSubDir = fileman.createSubFolders(projdir, configOptions['project-name'])

    # If sub directories don't exist, don't continue
    if createdSubDir == False:
        print("Error unable to create intermediate file directories")
        return

    # Get the project directory to pass to functions that follow
    # projdir = list(origFiles.values())[0].projDirectory

    fileman.copyReportFiles(projdir, configOptions['project-name'])

    # Generate Job script for step 1 and run all jobs
    prinseqJobIDS = []
    if (startStep == 1):
        prinseq.generateSLURMScript(origFiles, projdir, configOptions)
        prinseqJobIDS = prinseq.processAllFiles(projdir, configOptions, origFiles)
        startStep += 1

    # Generate Job script for step 2 and run all jobs
    bowtie2JobIDS = []
    if (startStep == 2):
        bowtie2.generateSLURMScirpt(origFiles, projdir, configOptions, prinseqJobIDS)
        bowtie2JobIDS = bowtie2.processAllFiles(projdir, configOptions, origFiles)
        startStep += 1

    # Generate Job script for step 3 and run all jobs
    samtoolsJobIDS = []
    if (startStep == 3):
        samtools.generateSLURMScript(origFiles, projdir, configOptions, bowtie2JobIDS)
        samtoolsJobIDS = samtools.processAllFiles(projdir, configOptions, origFiles)
        startStep += 1

    # Generate Job script for step 4 and run all jobs
    blastJobIDS = []
    if (startStep == 4):
        blast.generateSLURMScript(origFiles, projdir, configOptions, samtoolsJobIDS)
        blastJobIDS = blast.processAllFiles(projdir, configOptions, origFiles)
        startStep += 1

    # Generate Job script for step 5 and run all jobs
    emalPreJobIDS = []
    if (startStep == 5):
        emalPre = emal.generatePreScript(origFiles, projdir, configOptions, blastJobIDS)
        emalPreJobIDS = emal.processAllFiles(projdir, configOptions, origFiles, 1, emalPre)
        startStep += 1

    # Generate Job script for step 6 and run all jobs
    emalMainJobIDS = []
    if (startStep == 6):
        emalMain = emal.generateMainScript(origFiles, projdir, configOptions, emalPreJobIDS)
        emalMainJobIDS = emal.processAllFiles(projdir, configOptions, origFiles, 2, emalMain)
        startStep += 1

    # Generate Job script for step 7 and run all jobs
    emalPostJobIDS = []
    if (startStep == 7):
        emalPost = emal.generatePostScript(origFiles, projdir, configOptions, emalMainJobIDS)
        emalPostJobIDS = emal.processAllFiles(projdir, configOptions, origFiles, 3, emalPost)
        startStep += 1

    # Output file list and gather all results throughout the pipeline run and compile into final report
    outputFileList(origFiles, projdir, configOptions['project-name'])

    if not serialSample:
        final.collectPipelineResult(configOptions['project-name'], projdir, configOptions, emalPostJobIDS)
    else:
        print(configOptions['project-name'] + '-' + os.path.basename(os.path.normpath(projdir)))
        final.collectPipelineResult(configOptions['project-name'] + '-' + os.path.basename(os.path.normpath(projdir)),
                                    projdir, configOptions, emalPostJobIDS)

    print('\nAll required jobs for ' + inputFileDir + ' have been queued...\n')


# Main Function
if __name__ == "__main__":
    # Get all user set arguments before starting pipeline
    print("\nEzMap V1.0\n\nParsing config file...")
    allArgs = arguments.parseCommandLineArguments()
    configOptions = config.parseConfigOptions()

    # If a commandline option was set to provide a project name override the one within the config file to the
    # commandline project name
    if 'projectName' in allArgs:
        configOptions['project-name'] = allArgs['projectName']

    ensureScriptPermissions.checkForScriptPermisions(configOptions)

    startStep = int(configOptions['start-at-step'])

    if allArgs['serialSample'] == True:
        serialSample = True
        # Get list of directories within the sample directory
        for name in os.listdir(allArgs['directory']):
            if os.path.isdir(os.path.join(allArgs['directory'], name)):
                if not allArgs['directory'].endswith('/'):
                    allArgs['directory'] = allArgs['directory'] + '/'

                if not os.path.exists(allArgs['projDir'] + name):
                    print(allArgs['projDir'] + name)
                    os.mkdir(allArgs['projDir'] + name, 0o777)

                runEzMapOnTimePoint(configOptions, startStep, allArgs['directory'] + name, allArgs['projDir'] + name)

    else:
        runEzMapOnTimePoint(configOptions, startStep, allArgs['directory'], allArgs['projDir'])

    print('All required jobs have been created and queued...')
    print('You can now check the status of your jobs using the following command: ')
    print('squeue\n')
    print('Once those jobs have completed you can view your results in:\n' + allArgs['projDir'] + '6-FinalResult-' +
          configOptions['project-name'] + '/')
