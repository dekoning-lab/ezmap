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

    args = parser.parse_args()

    allArgs = {}
    allArgs['directory'] = args.directory
    allArgs['projDir'] = args.projDir

    return allArgs