__author__ = 'patrickczeczko'

import os
from scripts.datasetMember import datasetMember

class dataset:
    'this class will encompass the information relating to the entire dataset'
    samples = []
    projDir = ''

    def __init__(self, projDir):
        self.projDir = projDir

    # Create sub-directories in project folder
    def makeSubDirectories (self):
        if not os.path.isdir(self.projDir+'PRINSEQ-Results/'):
            os.mkdir(self.projDir+'PRINSEQ-Results/')
        if not os.path.isdir(self.projDir+'BowTie2-Results/'):
            os.mkdir(self.projDir+'BowTie2-Results/')
        if not os.path.isdir(self.projDir+'unMappedReads/'):
            os.mkdir(self.projDir+'unMappedReads/')
        if not os.path.isdir(self.projDir+'BLAST-Results/'):
            os.mkdir(self.projDir+'BLAST-Results/')

    # Create a dataset full of members from
    def generateDataSet (self, filedir):
        for file in os.listdir(filedir):
            if '.fastq' in file:
                sample = datasetMember (filedir)
                sample.createMemeber(file)
                self.samples.append(sample)

    def createFileListFile (self, type):
        if type == 'original':
            outfile = open (self.projDir+'originalFileList.txt','w+')
            for sample in self.samples:
                outfile.write(sample.filePath+sample.fileName)








