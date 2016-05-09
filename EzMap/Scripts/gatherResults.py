__author__ = 'patrickczeczko'

import sys, os, csv, time
from operator import itemgetter


def createProjectInfoFile(projName, projDir):
    outputfile = open(projDir + '6-FinalResult/information/projInfo.txt', 'w+')
    outputfile.write('projectName=' + projName)
    outputfile.write('\ndateRun=' + time.strftime("%d/%m/%Y"))
    outputfile.close()


def checkForExtraOptions(file):
    configFile = open(file, 'r')
    configOptions = {}
    for line in configFile:
        if '#extraTableSummedOver' in line:
            key, value = line.strip('#').split('=')
            configOptions[key] = value
    return configOptions


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

            percentGood = format((float(numGood) / numReads) * 100, '.3f')
            percentBad = format((float(numBad) / numReads) * 100, '.3f')
            prinseqInfo[fileID] = [fileID, numReads, avgReadLen, numGood, percentGood, numBad, percentBad]
    return prinseqInfo

def writePrinseqTableFile(dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(['Filename', '# Input Reads', 'Mean Read Length', '# Good Reads', '% Good Reads', '# Bad Reads',
                         '% Bad Reads'])

        for x in dict:
            writer.writerow(dict[x])
        del writer
        csvfile.close()


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
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(
            ['Filename', '# Reads', '# Reads Not Aligned', '# Reads Aligned Once', '# Reads Aligned Multiple'])
        for x in dict:
            writer.writerow(dict[x])
        csvfile.close()


def writeFileMappingDistribution(dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(['File', 'Human', 'Bacteria/Viruses'])
        for x in dict:
            if not isinstance(dict[x][1], str):
                totalNumReads = float(dict[x][1])
                totalHumanReads = float(dict[x][3]) + float(dict[x][4])
                totalNonHumanReads = float(dict[x][2])
                percentBacVir = (float(totalNonHumanReads / totalNumReads) * 100)
                percentHuman = (float(totalHumanReads / totalNumReads) * 100)
                writer.writerow([x, "%.10f" % percentHuman, "%.10f" % percentBacVir])


def getSamtoolsResults(fileDir):
    samtoolsInfo = {}
    for file in os.listdir(fileDir):
        if file.endswith('.fasta'):
            num_lines = int(sum(1 for line in open(fileDir + file)) / 2)
            filename = file.replace('.fasta', '')
            # filename = file.replace('-samtool.fasta', '')
            samtoolsInfo[filename] = [filename, num_lines]
    return samtoolsInfo


def writeSamtoolsTable(dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(
            ['Filename', '# of Non Human Reads'])
        for x in dict:
            writer.writerow(dict[x])
        csvfile.close()


def gatherBlastResults(fileDir):
    blastInfo = {}

    for file in os.listdir(fileDir):
        if file.endswith('.tsv'):
            fileName = file.replace('.tsv', '')
            # if file.endswith('-blastn.tsv'):
            #     fileName = file.replace('-blastn.tsv', '')
            num_lines = int(sum(1 for line in open(fileDir + file)))
            blastInfo[fileName] = [fileName, num_lines]

    return blastInfo


def writeBlastTable(dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(
            ['Filename', '# of Blast Hits'])
        for x in dict:
            writer.writerow(dict[x])
        csvfile.close()


def gatherEMALResults(fileDir):
    EMALInfo = []

    for file in os.listdir(fileDir):
        if file.endswith('-emal.csv'):
            openfile = open(fileDir + file, newline='')
            csvreader = csv.reader(openfile, delimiter=',', quotechar='"')
            for row in csvreader:
                row[5] = row[5].replace(',', '')
                EMALInfo.append(row)
    return EMALInfo


def writeEMALTable(list, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in list:
            writer.writerow(row)
        csvfile.close()


def writeEMALGraphInfo(infile, outfile):
    outfile = open(outfile, 'w+')

    with open(infile, newline='') as inputFile:
        for line in inputFile:
            reader = csv.reader(inputFile, delimiter=',', quotechar='"')
            for row in reader:
                outfile.write(row[2].split('[')[0] + '=' + row[3].split('[')[0] + '=' + row[4].split('[')[0] + '=' +
                              row[5].split('[')[0] + '=' + row[6].split('[')[0] + '=' + row[7].split('[')[0] + '=' +
                              row[1].split('[')[0] + ',' + row[0] + '\n')
    outfile.close()


def gatherSummedOverInfo(list, category):
    # name[taxonID] = GRA
    dict = {}

    index = -1
    for i, item in enumerate(list[0]):
        # Remove possible newline characters that could break the comparison
        category = category.strip()
        item = item.strip()
        if category == item:
            index = i

    if (index != -1):
        list.pop(0)
        for x in list:
            key = x[index]
            if key in dict:
                GRA = dict[key]
                GRA += float(x[0])
                dict[key] = GRA
            else:
                dict[key] = float(x[0])

    return dict

def writeSummedOverInfo(category, dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['GRA',category])
        for key in dict:
            writer.writerow([dict[key],key])
        csvfile.close()


if __name__ == "__main__":
    projDir = sys.argv[1]
    projName = sys.argv[2]
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')
    configOptions = checkForExtraOptions(cwd + 'param.config')
    createProjectInfoFile(projName, projDir)
    print('Gathering Step 1 Results...')
    prinseqInfo = getPRINSEQResults(projDir + '1-Cleaning/')
    writePrinseqTableFile(prinseqInfo, projDir + '6-FinalResult/information/' + 'prinseq-tbl-1.csv')
    print('Gathering Step 2 Results...')
    bowtieInfo = getBowtie2Results(projDir + '2-HumanMapping/')
    writeBowtieTableFile(bowtieInfo, projDir + '6-FinalResult/information/' + 'bowtie2-tbl-1.csv')
    writeFileMappingDistribution(bowtieInfo, projDir + '6-FinalResult/information/' + 'mappedto.csv')
    print('Gathering Step 3 Results...')
    samtoolsInfo = getSamtoolsResults(projDir + '3-UnmappedCollection/')
    writeSamtoolsTable(samtoolsInfo, projDir + '6-FinalResult/information/' + 'samtools-tbl-1.csv')
    print('Gathering Step 4 Results...')
    blastInfo = gatherBlastResults(projDir + '4-OrganismMapping/')
    writeBlastTable(blastInfo, projDir + '6-FinalResult/information/' + 'blastn-tbl-1.csv')
    print('Gathering Step 5 Results...')
    emalInfo = gatherEMALResults(projDir + '5-RelativeAbundanceEstimation/')
    print(emalInfo)
    writeEMALTable(emalInfo, projDir + '6-FinalResult/information/' + 'emal-tbl-1.csv')
    writeEMALGraphInfo(projDir + '6-FinalResult/information/' + 'emal-tbl-1.csv',
                       projDir + '6-FinalResult/information/' + 'emal-graph-1.csv')
    summedOver = gatherSummedOverInfo(emalInfo, configOptions['extraTableSummedOver'])
    writeSummedOverInfo(configOptions['extraTableSummedOver'], summedOver, projDir + '6-FinalResult/information/' + 'emal-tbl-2.csv')

    print('Complete!')