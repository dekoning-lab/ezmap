__author__ = 'patrickczeczko'

import os
from Scripts.dataset import Dataset

# Create Subdirectories for all the intermediate files
def createSubFolders(projDir):
    if os.path.exists(projDir):
        print('Creating Sub directories in ' + projDir)
        if not os.path.exists(projDir + '/1-Cleaning/'):
            os.mkdir(projDir + '/1-Cleaning/')
        if not os.path.exists(projDir + '/2-HumanMapping/'):
            os.mkdir(projDir + '/2-HumanMapping/')
        if not os.path.exists(projDir + '/3-UnmappedCollection/'):
            os.mkdir(projDir + '/3-UnmappedCollection/')
        if not os.path.exists(projDir + '/4-OrganismMapping/'):
            os.mkdir(projDir + '/4-OrganismMapping/')
        if not os.path.exists(projDir + '/5-RelativeAbundanceEstimation/'):
            os.mkdir(projDir + '/5-RelativeAbundanceEstimation/')
        if not os.path.exists(projDir + '/6-FinalResult/'):
            os.mkdir(projDir + '/6-FinalResult/')
        return True
    return False

# return a dictionary of dataset objects corressponding to each file
def getListOfOriginalFiles(fileDir,projDir):
    origfiles = {}
    for file in os.listdir(fileDir):
        if file.endswith('.fq') or file.endswith('.fastq'):
            root, ext = os.path.splitext(file)
            origfiles[root] = (Dataset(file, fileDir,projDir))
    return origfiles
