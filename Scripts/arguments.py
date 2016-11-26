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
    parser.add_argument("-pn", "--projectName", type=str, required=False,
                        help="Set the project name from the commandline and override the one provided in the config "
                             "file.")
    parser.add_argument("-dm", "--desktopMode",action="store_true", required=False,
                        help="Setting this will run ezmap in a single node mode that does not require a job manager. "
                             "This intended for the use of ezmap on a single workstation")

    args = parser.parse_args()

    allArgs = {}

    allArgs['directory'] = args.directory
    if args.projDir.endswith("/"):
        allArgs['projDir'] = args.projDir
    else:
        allArgs['projDir'] = args.projDir + '/'

    allArgs['serialSample'] = False
    if args.serialSample == True:
        allArgs['serialSample'] = True

    if args.projectName:
        allArgs['projectName'] = args.projectName

    allArgs['desktopMode'] = False
    if args.desktopMode == True:
        allArgs['desktopMode'] = True

    return allArgs
