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
    # PRINSEQ Arguments
    parser.add_argument("-pof", "--prinseq-out_format", type=int, required=True,
                        help="Output format"
                             "1 (FASTA only), 2 (FASTA and QUAL), 3 (FASTQ), 4 (FASTQ and FASTA), 5 (FASTQ, FASTA and "
                             "QUAL)")
    parser.add_argument("-pmqs", "--prinseq-min_qual_score", type=int, required=True,
                        help="Filter sequence with at least one quality score below min_qual_score")
    parser.add_argument("-plm", "--prinseq-lc_method", type=str, required=True,
                        help="Method to filter low complexity sequences - [dust, entropy]")
    parser.add_argument("-plt", "--prinseq-lc_threshold", type=int, required=True,
                        help="The threshold value used to filter sequences by sequence complexity. The dust method "
                             "uses this as maximum allowed score and the entropy method as minimum allowed value. "
                             "INT [0..100]")

    args = parser.parse_args()

    allArgs = {}
    allArgs['directory'] = args.directory
    allArgs['projDir'] = args.projDir

    return allArgs
