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
    prinseqJobID = prinseq.processAllFiles(len(origFiles), projdir)

    # Update the prinseq jobID for all datasets
    for x in origFiles:
        origFiles[x].updateJobID(1, prinseqJobID)

    print('EXITING...')
