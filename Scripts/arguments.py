__author__ = 'patrickczeczko'

import argparse

# Parses the command line arguments to determine where the input and output files are located
def parseCommandLineArguments():
    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="Provide a complete path to a directory containing the files of Raw Sequence Information")
    parser.add_argument("-p", "--projDir", type=str, required=True,
                        help="Provide a complete path to a directory where all intermediate files and folders will "
                             "be placed")
    parser.add_argument("-s", "--serialSample" ,action="store_true", required=False,
                        help="Setting this method means that each of the directories in -d will contain a sample time "
                             "point and should therefore be run individually")

    args = parser.parse_args()

    allArgs = {}
    allArgs['directory'] = args.directory
    if args.projDir.endswith("/"):
        allArgs['projDir'] = args.projDir
    else:
        allArgs['projDir'] = args.projDir + '/'

    if args.serialSample == True:
        allArgs['serialSample'] = True
    else:
        allArgs['serialSample'] = False

    return allArgs
