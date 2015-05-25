__author__ = 'patrickczeczko'

import argparse
import os
import Dataset
import time

# Function to create all command line arguments that are accepted
def createArguments ():
    parser = argparse.ArgumentParser(description='Enable the determination of viral genomic abundance from DNA samples')

    # File Directory Argument
    parser.add_argument('--fileDir','-f', nargs='?'
                        ,help='Absolute file path to the directory containing all FASTQ files to be analyzed')
    return parser

# This Function will get a ist of all FATSQ Files in directory
# Returns: List of Dataset Objects
def getListOfFiles (dir):
    files = []

    print("Searching for FASTQ files in "+dir)
    time.sleep(2)

    for file in os.listdir(dir):
        if file.endswith('.fastq') & (not "prinseq" in file):
            dataSet = Dataset.Dataset

            dataSet.fileName = file
            dataSet.filePath = dir

            if os.path.exists(dir+file+'.log'):
                dataSet.prinseqLogFile = file+'.log'

            files.append(dataSet)

    print(str(len(files))+" FASTQ files found to analyze")
    time.sleep(3)

    return files

def checkForPRINSEQLogs (datasets):
    print("Checking for PRINSEQ log files")
    time.sleep(2)
    for dataset in datasets:
        if dataset.prinseqLogFile == "":
            return False
    return True

def createPRINSEQjobs (datasets):
    for dataset in datasets:
        if dataset.prinseqLogFile == "":
            print("Creating SLURM Jobs")


# Main Function
if __name__ == "__main__":
    parser = createArguments()
    args = parser.parse_args()

    dir = args.fileDir

    datasets = getListOfFiles(str(dir))

    if checkForPRINSEQLogs(datasets) == False:
        print("PRINSEQ log files missing")
    else:
        print("All PRINSEQ log files found")









