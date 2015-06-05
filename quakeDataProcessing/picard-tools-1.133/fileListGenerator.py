import os, sys

infiledir = sys.argv[1]

fileList = []

for file in os.listdir(infiledir):
    if '.unmapped.sam' in file:
        fileList.append(file)

print(fileList)




