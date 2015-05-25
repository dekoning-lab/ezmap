# ===================================================================
# Viral Metagenomics Abundance Pipeline (VMAP)
#
# Author: Patrick Czeczko @ University of Calgary (de Koning Lab)
# Version: 0.1
#
# Description:
#
# The intent of this pipeline is to enable the identification of
# viral composition within a sample of DNA.
# ===================================================================

__author__ = 'patrickczeczko'

import arguments
import prinseq

# Main Function
if __name__ == "__main__":
    parser = arguments.createArguments()
    args = parser.parse_args()

    dir = args.fileDir

    f = open('version.txt','r')
    print(f.read())

    datasets = prinseq.getListOfFiles(str(dir))

    if prinseq.checkForPRINSEQLogs(datasets) == False:
        print("\nPRINSEQ log files missing\n")
        print("SLURM Jobs will be created to process the following files:")
        prinseq.createPRINSEQjobs(datasets,dir)
    else:
        print("All PRINSEQ log files found")

    print('\n')









