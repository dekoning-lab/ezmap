__author__ = "patrickczeczko"

import os
import sys
import subprocess

inFileDir = sys.argv[1]

fileList = []

for file in os.listdir(inFileDir):
    if ".sam" in file:
        fileList.append(file)

print(fileList)

