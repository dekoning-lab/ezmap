import os
import subprocess

import dataset

__author__ = 'patrickczeczko'

# This Function will get a ist of all FATSQ Files in directory
# Returns: List of Dataset Objects
def getListOfFiles (dir):
    files = []

    print("\nSearching for FASTQ files in "+dir+'...')

    for file in os.listdir(dir):
        if file.endswith('.fastq') & (not "prinseq" in file):
            dataSet = dataset.Dataset

            dataSet.fileName = file
            dataSet.filePath = dir

            if os.path.exists(dir+file+'.log'):
                dataSet.prinseqLogFile = file+'.log'

            files.append(dataSet)

    print(str(len(files))+" FASTQ files found to analyze")

    return files

def checkForPRINSEQLogs (datasets):
    print("\nChecking for PRINSEQ log files...")
    for dataset in datasets:
        if dataset.prinseqLogFile == "":
            return False
    return True

def createPRINSEQjobs (datasets,dir):
    datasetsToProcess = []
    for dataset in datasets:
        if dataset.prinseqLogFile == "":
            datasetsToProcess.append(dataset.fileName)

    print(datasetsToProcess)
    subprocess.Popen(['sh','prinseqIndividualScript.sbatch','-p',dir])