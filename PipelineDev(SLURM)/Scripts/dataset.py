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


