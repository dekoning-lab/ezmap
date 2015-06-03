from __future__ import division
import os


filesDir = "/hyperion/work/patrick/quakeDataMapping/"

numOfReads = 0
numNotAligned = 0
numAlignedOnce = 0
numAlignMulti = 0

for fileName in os.listdir(filesDir):
    if '.errs' in fileName:
        file = open(fileName)
        line = file.readline()
        if 'reads; of these:' in line:
            line = file.readline()
            numOfReads += int(line.split()[0])

            line = file.readline()
            numNotAligned += int(line.split()[0])

            line = file.readline()
            numAlignedOnce += int(line.split()[0])

            line = file.readline()
            numAlignMulti += int(line.split()[0])

print(str(numOfReads)+' reads; of these:')
print(str(numNotAligned)+' ('+str((numNotAligned/numOfReads)*100)+') '+'aligned 0 times')
print(str(numAlignedOnce)+' ('+str((numAlignedOnce/numOfReads)*100)+') '+' aligned exactly 1 time')
print(str(numAlignMulti)+' ('+str((numAlignMulti/numOfReads)*100)+') '+' aligned >1 times')








