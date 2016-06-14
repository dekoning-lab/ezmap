__author__ = 'patrickczeczko'

import os, sys
import subprocess
import shlex


def execute(command, filename, outputDir, filterLen):
    print(outputDir + filename + '.tsv')
    outputFile = open(outputDir + filename + '.tsv', 'w+')
    popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        line = line.decode()
        if int(line.split('\t')[3]) >= filterLen:
            outputFile.write(line)

# System Arguments
# 1 - path to blastn
# 2 - path to balst database
# 3 - path to query file
# 4 - csv string of parameters and values
# 5 - directory to output file
# 6 - filter length to use for file
if __name__ == "__main__":
    blastnPath = sys.argv[1]
    databasePath = sys.argv[2]
    queryPath = sys.argv[3]
    options = sys.argv[4].split(',')
    outputDir = sys.argv[5]
    filterLen = int(sys.argv[6])
    outputName = sys.argv[7]

    command = blastnPath
    command += ' -db ' + databasePath
    command += ' -query ' + queryPath

    for x in range(0, len(options), 2):
        command += ' -' + options[x] + ' ' + options[x + 1]

    commmand = shlex.split(command)

    if filterLen < 0:
        filterLen = 0

    execute(command, outputName, outputDir, filterLen)
