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
    # PRINSEQ Arguments
    parser.add_argument("-pof", "--prinseq-out_format", type=int,
                        help="Output format"
                             "1 (FASTA only), 2 (FASTA and QUAL), 3 (FASTQ), 4 (FASTQ and FASTA), 5 (FASTQ, FASTA and "
                             "QUAL). Default: 3")
    parser.add_argument("-pmqs", "--prinseq-min_qual_score", type=int,
                        help="Filter sequence with at least one quality score below min_qual_score.  Default: 21")
    parser.add_argument("-plm", "--prinseq-lc_method", type=str,
                        help="Method to filter low complexity sequences - [dust, entropy].  Default: dust")
    parser.add_argument("-plt", "--prinseq-lc_threshold", type=int,
                        help="The threshold value used to filter sequences by sequence complexity. The dust method "
                             "uses this as maximum allowed score and the entropy method as minimum allowed value. "
                             "INT [0..100] Default: 7")


    args = parser.parse_args()

    allArgs = {}
    allArgs['directory'] = args.directory
    allArgs['projDir'] = args.projDir
    allArgs['maxThreads'] = args.maxThreads

    return allArgs
