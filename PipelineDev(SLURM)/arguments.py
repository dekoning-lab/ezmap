__author__ = 'patrickczeczko'

import argparse

# Function to create all command line arguments that are accepted
def createArguments ():
    parser = argparse.ArgumentParser(description='Enable the determination of viral genomic abundance from DNA samples')

    # File Directory Argument
    parser.add_argument('--fileDir','-f', nargs='?'
                        ,help='Absolute file path to the directory containing all FASTQ files to be analyzed')
    parser.add_argument('-out_format',nargs='?',
                        help='Output format 1 (FASTA only), 2 (FASTA and QUAL), 3 (FASTQ), 4 (FASTQ and FASTA), 5 (FASTQ, FASTA and QUAL)')
    parser.add_argument('-min_qual_score',nargs='?',
                        help='Filter sequence with at least one quality score below min_qual_score')
    parser.add_argument('--lc_method',nargs='?',
                        help='Method to filter low complexity sequences (\'dust\',\'entropy\')')
    parser.add_argument('--lc_threshold',nargs='?',
                        help='The threshold value used to filter sequences by sequence complexity. The dust method uses this as maximum allowed score and the entropy method as minimum allowed value')


    return parser