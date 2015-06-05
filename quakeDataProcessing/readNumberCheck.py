__author__ = 'patrickczeczko'

import os
import subprocess

def getNumOfFASTQReads (dir,file):
    args = ['wc','-l',dir+file]

    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    out, err = proc.communicate()

    return int(out.split(" ")[0])/4

def getNumOfSAMReads (dir,file):
    args = ['wc','-l',dir+file]

    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    out, err = proc.communicate()

    return (int(out.split(" ")[0]))


fastqFilesDir = '/hyperion/work/patrick/quakeData/unmappedFASTQ/'
samFileDir = '/hyperion/work/patrick/quakeData/unmappedSAM/'

outFile = open('fileCompare.txt','w+')

for file in os.listdir(samFileDir):
    fastqNUM = 0
    samNUM = -1
    if '.unmapped.sam' in file:
        fileID = file[0:10]

        fastqNUM = getNumOfFASTQReads(fastqFilesDir,fileID+'.fastq')
        samNUM = getNumOfSAMReads(samFileDir,file)

        if fastqNUM != samNUM:
            outFile.write(fileID+' '+str(samNUM)+' != '+str(fastqNUM))
        else:
            outFile.write(fileID+' correct '+str(samNUM)+' == '+str(fastqNUM))







