# ===================================================================
# Viral Metagenomics Abundance Pipeline (VMAP)
#
# Author: Patrick Czeczko @ de Koning Lab
# Version: 0.1
#
# ===================================================================

__author__ = 'patrickczeczko'

from scripts import arguments
from scripts.dataset import dataset
from scripts import prinseq

# Main Function
if __name__ == "__main__":
    # Get all arguments
    parser = arguments.createArguments()
    args = parser.parse_args()

    # Determine the directory files are located in
    filedir = args.fileDir
    projdir = args.projDir

    # Generate a data set of all files
    allFiles = dataset(projdir)
    allFiles.makeSubDirectories()
    allFiles.generateDataSet(filedir)

    print(allFiles.samples[0].filePath)

    allFiles.createFileListFile('original')

























