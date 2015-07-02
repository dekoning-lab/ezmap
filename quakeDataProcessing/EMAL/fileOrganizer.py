__author__ = 'patrickczeczko'

import os
import time

allInformation = {}
fileName = "/hyperion/work/patrick/quakeDataProcessing/EMAL/new.xml"
SRRFileDirPath = "/hyperion/work/patrick/quakeData/BLASTResults/"
outputFile = open('new.csv', 'w+')

MPTList = []
infile = open(fileName, 'r')
count = 0
SRR = ''
MPT = ''
start = 4762

for line in infile:
    if ('SRR' in line) and ('</PRIMARY_ID>' in line):
        SRR = line.strip('\n\t</PRIMARY_ID>                    ')
        outputFile.write(SRR+','+MPT+',\n')
        allInformation[SRR] = float(MPT)
        MPTList.append(float(MPT))

    elif 'Months_post_transplant</TAG>' in line:
        count = 0
    elif count == 2:
        MPT = line.strip('\n\t                    </VALUE>')
    count += 1

MPTList = sorted(set(MPTList))

for x in MPTList:
    if not os.path.isdir(SRRFileDirPath+'MPT'+str(x)):
        os.mkdir(SRRFileDirPath+'MPT'+str(x))

for file in os.listdir(SRRFileDirPath):
    if file.endswith('.txt'):
        filename = file.strip('.txt')

        src = SRRFileDirPath+file
        dst = SRRFileDirPath+'MPT'+str(allInformation[filename])+'/'+filename+'.tblat'

        os.rename(src,dst)
        print('Moved '+src+' to '+dst)

