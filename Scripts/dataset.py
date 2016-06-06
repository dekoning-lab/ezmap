__author__ = 'patrickczeczko'

import os


class Dataset:
    # Original File Information
    origFilePath = ""
    origFileName = ""

    # Information on where intermediate files should be placed
    projDirectory = ""

    # Information based on what output files should be named
    prinseqOutputName = ""
    bowtie2OutputName = ""
    samtoolsOutputName = ""
    blastnOutputName = ""
    EMALOutputName = ""

    prinseqJobID = 0
    bowtie2JobID = 0
    samtoolsJobID = 0
    blastnJobID = 0
    EMALJobID = 0

    # Gather initial information
    def __init__(self, origfilename, filepath, projdir):
        self.origFileName = origfilename
        self.origFilePath = filepath
        self.projDirectory = projdir

        self.generateOutputFileNames()

    # Generate names for intermediate files
    def generateOutputFileNames(self):
        root, ext = os.path.splitext(self.origFileName)

        self.prinseqOutputName = root + "-prinseq"
        self.bowtie2OutputName = root + "-bwt2"
        self.samtoolsOutputName = root + "-samtool"
        self.blastnOutputName = root + "-blastn"
        self.EMALOutputName = root + "-emal"

    def updateJobID(self, step, ID):
        if step == 1:
            self.prinseqJobID = ID
        elif step == 2:
            self.bowtie2JobID = ID
        elif step == 3:
            self.samtoolsJobID = ID
        elif step == 4:
            self.blastnJobID = ID
        elif step == 5:
            self.EMALJobID = ID
