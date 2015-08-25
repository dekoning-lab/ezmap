__author__ = 'patrickczeczko'

import argparse


def parseCommandLineArguments():
    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="Provide a complete path to a directory containing the files of Raw Sequence Information")
    parser.add_argument("--projDir", type=str, required=True,
                        help="Provide a complete path to a directory where all intermediate files and folders will "
                             "be placed")
    parser.add_argument("-mt", "--maxThreads", type=str, required=True,
                        help="The maximum number of threads allowed to run concurrently at any point. Default: 1")

    args = parser.parse_args()

    allArgs = {}
    allArgs['directory'] = args.directory
    if args.projDir.endswith("/"):
        allArgs['projDir'] = args.projDir
    else:
        allArgs['projDir'] = args.projDir + '/'
    allArgs['maxThreads'] = args.maxThreads

    return allArgs
