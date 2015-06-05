__author__ = 'patrickczeczko'

import os

inFileDir = '/hyperion/work/patrick/quakeData/unmappedFASTQ/'
outFileDir = '/hyperion/work/patrick/quakeData/unmappedSAM/'

for file in os.listdir(outFileDir):
    if '.sam' in file:
        fileID = file[0:10]
        if not os.path.exists(inFileDir+fileID):
            print(fileID+' missing')
