__author__ = 'patrickczeczko'

import sys, os


def getPRINSEQResults(fileDir):
    prinseqInfo = {}

    for file in os.listdir(fileDir):
        if file.endswith('.err'):
            inFile = open(fileDir + file, 'r')

            output = open(fileDir + os.path.splitext(file)[0] + '.out')
            fileID = output.readline().split(' ')[0]

            for line in inFile:
                if 'Input sequences:' in line:
                    numReads = int(line.split(':')[1].strip().replace(',', ''))
                elif 'Input mean length:' in line:
                    avgReadLen = float(line.split(':')[1].strip().replace(',', ''))
                elif 'Good sequences:' in line:
                    numGood = int(line.split('(')[0].split(':')[1].strip().replace(',', ''))
                elif 'Bad sequences:' in line:
                    numBad = int(line.split('(')[0].split(':')[1].strip().replace(',', ''))
            prinseqInfo[fileID] = [fileID, numReads, avgReadLen, numGood, numBad]
    return prinseqInfo


def writePrinseqTableFile(dict, outfile):
    output = open(outfile, 'w+')

    output.write(
        '<table class="table table-striped table-bordered"><thead><tr><td>Filename</td><td># Input Reads</td><td>Mean Seq. Reads</td>'
        '<td># Good Reads</td><td># Bad Reads</td></tr></thead>')

    output.write('<tbody>')
    for x in dict:
        output.write('<tr>' +
                     '<td>' + str(dict[x][0]) + '</td>' +
                     '<td>' + str(dict[x][1]) + '</td>' +
                     '<td>' + str(dict[x][2]) + '</td>' +
                     '<td>' + str(dict[x][3]) + '</td>' +
                     '<td>' + str(dict[x][4]) + '</td>' +
                     '</tr>')
    output.write('</tbody></table>')


def getBowtie2Results(fileDir):
    bowtieInfo = {}
    for file in os.listdir(fileDir):
        if file.endswith('.err'):
            inFile = open(fileDir + file, 'r')

            output = open(fileDir + os.path.splitext(file)[0] + '.out')
            fileID = output.readline().split(': ')[1].split('-')[0]
            zeroAlign, oneAlign, multiAlign = -1, -1, -1
            for line in inFile:
                if 'reads; of these:' in line:
                    numReads = int(line.split(' read')[0].strip().replace(',', ''))
                elif 'aligned 0 times' in line:
                    zeroAlign = float(line.split('(')[0].strip().replace(',', ''))
                elif 'aligned exactly 1 time' in line:
                    oneAlign = float(line.split('(')[0].strip().replace(',', ''))
                elif 'aligned >1 times' in line:
                    multiAlign = float(line.split('(')[0].strip().replace(',', ''))
            if zeroAlign == -1 and oneAlign == -1 and multiAlign == -1:
                bowtieInfo[fileID] = [fileID, 'N/A', 'N/A', 'N/A', 'N/A']
            else:
                bowtieInfo[fileID] = [fileID, numReads, zeroAlign, oneAlign, multiAlign]

    return bowtieInfo


def writeBowtieTableFile(dict, outfile):
    output = open(outfile, 'w+')

    output.write(
        '<table class="table table-striped table-bordered"><thead><tr><td>Filename</td><td># Reads</td><td># Reads Not Aligned</td>'
        '<td># Reads Aligned Once</td><td># Reads Aligned Multiple</td></tr></thead>')

    output.write('<tbody>')
    for x in dict:
        output.write('<tr>' +
                     '<td>' + str(dict[x][0]) + '</td>' +
                     '<td>' + str(dict[x][1]) + '</td>' +
                     '<td>' + str(dict[x][2]) + '</td>' +
                     '<td>' + str(dict[x][3]) + '</td>' +
                     '<td>' + str(dict[x][4]) + '</td>' +
                     '</tr>')
    output.write('</tbody></table>')


if __name__ == "__main__":
    projDir = sys.argv[1]
    prinseqInfo = getPRINSEQResults(projDir + '1-Cleaning/')
    writePrinseqTableFile(prinseqInfo, projDir + '6-FinalResult/information/' + 'prinseq-tbl-1.txt')
    bowtieInfo = getBowtie2Results(projDir + '2-HumanMapping/')
    writeBowtieTableFile(bowtieInfo, projDir + '6-FinalResult/information/' + 'bowtie2-tbl-1.txt')
