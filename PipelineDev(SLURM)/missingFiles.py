import os
import sys

def getMissedFiles():
    dir = sys.argv[1]

    countMissingFiles = 0
    countTotalFiles = 0
    fileName = ''

    arrayOfMissingFiles = []

    for file in os.listdir(dir):
        if file.endswith(".fastq") & (not "prinseq" in file):
            if not os.path.exists(dir+file+'.log'):
                 arrayOfMissingFiles.append(file)

    return arrayOfMissingFiles

print(getMissedFiles())