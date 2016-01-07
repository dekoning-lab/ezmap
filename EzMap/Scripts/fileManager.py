__author__ = 'patrickczeczko'

import os
from Scripts.dataset import Dataset
from distutils.dir_util import copy_tree

# Create Subdirectories for all the intermediate files
def createSubFolders(projDir):
    if not os.path.exists(projDir):
        os.mkdir(projDir, 0o777)

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
        if not os.path.exists(projDir + '/6-FinalResult/information/'):
            os.mkdir(projDir + '/6-FinalResult/information/')
        return True
    return False


# return a dictionary of dataset objects corressponding to each file
def getListOfOriginalFiles(fileDir, projDir):
    origfiles = {}
    for file in os.listdir(fileDir):
        if file.endswith('.fq') or file.endswith('.fastq'):
            root, ext = os.path.splitext(file)
            origfiles[root] = (Dataset(file, fileDir, projDir))
    return origfiles


def copyReportFiles(projDir):
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')
    copy_tree(cwd + 'ReportFiles', projDir + '6-FinalResult')
