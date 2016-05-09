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
import sys

import Scripts.arguments as arguments
import Scripts.configOptions as config
import Scripts.fileManager as fileman
import Scripts.prinseqPrep as prinseq
import Scripts.bowtie2Prep as bowtie2
import Scripts.samtoolsPrep as samtools
import Scripts.blastprep as blast
import Scripts.emalPrep as emal
import Scripts.finalScript as final

# Cretaes a txt file of all importnat output files for final report
def outputFileList(files, projDir):
    outputfile = open(projdir + '6-FinalResult/information/' + 'filelist.txt', 'w+')
    outputfile.write(
        '<table class="table table-striped table-bordered"><thead><tr><td>Filename</td><td>Path</td></tr></thead>')

    outputfile.write('<tbody>')
    for x in files:
        outputfile.write('<tr><td>' + files[x].origFileName + '</td><td>' + files[x].origFilePath.replace('/',
                                                                                                          '&#47;') + '</td></tr>')
    outputfile.write('</tbody></table>')

# Main Function
if __name__ == "__main__":
    # Get all user set arguments before starting pipeline
    print("Starting EzMap \n\nParsing config file...")
    allArgs = arguments.parseCommandLineArguments()
    configOptions = config.parseConfigOptions()
    startStep = int(configOptions['start-at-step'])

    # Get list of FASTQ files to process
    origFiles = fileman.getListOfOriginalFiles(allArgs['directory'], allArgs['projDir'])

    # Check if there is at least one file to process
    if len(origFiles) < 1:
        print('No files found to process!')
        print('Exiting...')
        sys.exit()

    # Create subdirectories where intermediate files will live
    createdSubDir = fileman.createSubFolders(allArgs['projDir'])
    # If sub directories don't exist, don't continue
    if createdSubDir == False:
        print("Error unable to create intermediate file directories")
        sys.exit()

    # Get the project directory to pass to functions that follow
    projdir = list(origFiles.values())[0].projDirectory

    fileman.copyReportFiles(projdir)

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
    outputFileList(origFiles, projdir)
    final.collectPipelineResult(configOptions['project-name'], projdir, configOptions, emalPostJobIDS)

    print('All required jobs have been created and queued...\nEXITING...')