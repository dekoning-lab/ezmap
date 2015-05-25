__author__ = 'patrickczeczko'

class Dataset:
    'this class will encompass the information relating to a single data set file'

    ranPRINSEQ = False
    ranMapping = False

    #Basic file information
    filePath = ""
    fileName = ""
    prinseqLogFile = ""

    #Information from PRINSEQ cleaning
    totalNumSeq = -1
    totalGoodSeq = -1
    totalBadSeq = -1
    totalLowQualSeq = -1



