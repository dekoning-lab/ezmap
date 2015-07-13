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
import Scripts.fileManager as fileman
import Scripts.prinseqPrep as prinseq

# Main Function
if __name__ == "__main__":
    # Get all user set arguments before starting pipeline
    allArgs = arguments.parseCommandLineArguments()

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
        sys.exit()

    projdir = list(origFiles.values())[0].projDirectory
    prinseq.generateSLURMScript(origFiles, projdir)

    print('EXITING...')

