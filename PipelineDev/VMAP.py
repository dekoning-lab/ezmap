# ===================================================================
# Viral Metagenomics Abundance Pipeline (VMAP)
#
# Author: Patrick Czeczko @ de Koning Lab
# Version: 0.1a
#
# ===================================================================

__author__ = 'patrickczeczko'
import sys

import Scripts.arguments as arguments
import Scripts.configOptions as config
import Scripts.fileManager as fileman
import Scripts.prinseqPrep as prinseq
import Scripts.bowtie2Prep as bowtie2
import Scripts.samtoolsPrep as samtools

import Scripts.finalScript as final


def outputFileList(files, projDir):
    outputfile = open(projdir + '6-FinalResult/information/' + 'filelist.txt', 'w+')
    outputfile.write('<table class="table table-striped table-bordered"><thead><tr><td>Filename</td></tr></thead>')

    outputfile.write('<tbody>')
    for x in files:
        outputfile.write('<tr><td>' + files[x].origFileName + '</td></tr>')
    outputfile.write('</tbody></table>')

# Main Function
if __name__ == "__main__":
    # Get all user set arguments before starting pipeline
    allArgs = arguments.parseCommandLineArguments()
    configOptions = config.parseConfigOptions()

    # Create subdirectories where intermediate files will live
    createdSubDir = fileman.createSubFolders(allArgs['projDir'])
    # If sub directories don't exist, don't continue
    if createdSubDir == False:
        print("Error unable to create intermediate file directories")
        sys.exit()

    # Get list of FASTQ files to process
    origFiles = fileman.getListOfOriginalFiles(allArgs['directory'], allArgs['projDir'])

    # Check if there is at least one file to process
    if len(origFiles) < 1:
        print('No files found to process!')
        sys.exit()

    # Get the project directory to pass to functions that follow
    projdir = list(origFiles.values())[0].projDirectory

    # Generate Job script for step 1 and run all jobs
    prinseq.generateSLURMScript(origFiles, projdir, configOptions)
    prinseqJobIDS = prinseq.processAllFiles(projdir, configOptions, origFiles)

    # Generate Job script for step 2 and run all jobs
    bowtie2.generateSLURMScirpt(origFiles, projdir, configOptions, allArgs['maxThreads'], prinseqJobIDS)
    bowtie2JobIDS = bowtie2.processAllFiles(projdir, configOptions, origFiles)

    # Generate Job script for step 3 and run all jobs
    samtools.generateSLURMScript(origFiles, projdir, configOptions, bowtie2JobIDS)
    samtoolsJobIDS = samtools.processAllFiles(projdir, configOptions, origFiles)

    outputFileList(origFiles, projdir)
    final.collectPipelineResult(projdir, configOptions, samtoolsJobIDS)

    print('EXITING...')
