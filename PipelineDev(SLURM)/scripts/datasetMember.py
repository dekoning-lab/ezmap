__author__ = 'patrickczeczko'

import os

class datasetMember:
    'this class will contain information relating to a single data file'

    filePath = ''
    fileName = ''

    def __init__(self, filepath):
        self.filePath = filepath

    def createMemeber (self,filename):
        self.fileName = filename





