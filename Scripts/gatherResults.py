#__author__ = 'patrickczeczko'

import sys, os, csv, time, json
from Bio import Entrez
from operator import itemgetter


# Generate a file with the required project info to display pipeline results
def createProjectInfoFile(projName, projDir):
    outputfile = open(projDir + '6-FinalResult-'+projName+'/information/projInfo.txt', 'w+')
    outputfile.write('projectName=' + projName)
    outputfile.write('\ndateRun=' + time.strftime("%d/%m/%Y %X"))
    outputfile.close()


# Check to see a additional summary graph should be generated based on a specific taxonomic level
def checkForExtraOptions(file):
    configFile = open(file, 'r')
    configOptions = {}
    for line in configFile:
        if '>extraTableSummedOver' in line:
            key, value = line.strip('>').split('=')
            configOptions[key] = value
    return configOptions


# Gather all of the results related to PRINSEQ
def getPRINSEQResults(fileDir):
    prinseqInfo = {}

    for file in os.listdir(fileDir):
        if file.endswith('.log'):
            inFile = open(fileDir + file, 'r')
            # output = open(fileDir + os.path.splitext(file)[0] + '.out')
            # fileID = output.readline().split(' ')[0]
            for line in inFile:
                fileID = file.split('-prinseq')[0]
                if 'Input sequences:' in line:
                    numReads = int(line.split('Input sequences:')[1].strip().replace(',', ''))
                elif 'Input mean length:' in line:
                    avgReadLen = float(line.split('Input mean length:')[1].strip().replace(',', ''))
                elif 'Good sequences:' in line:
                    numGood = int(line.split('(')[0].split('Good sequences:')[1].strip().replace(',', ''))
                elif 'Bad sequences:' in line:
                    numBad = int(line.split('(')[0].split('Bad sequences:')[1].strip().replace(',', ''))

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
        if file.endswith('.err') or file.endswith('.errs'):
            inFile = open(fileDir + file, 'r')
            output = open(fileDir + os.path.splitext(file)[0] + '.out')

            fileID = output.readline().split(': ')[1].rstrip('\n').replace("\"","")

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

        writer.writerow(['File', 'Human', 'Non-Human'])
        for x in dict:
            if not isinstance(dict[x][1], str):
                totalNumReads = float(dict[x][1])
                totalHumanReads = float(dict[x][3]) + float(dict[x][4])
                totalNonHumanReads = float(dict[x][2])
                percentBacVir = (float(totalNonHumanReads / totalNumReads) * 100)
                percentHuman = (float(totalHumanReads / totalNumReads) * 100)

                x = x.rstrip('\n')
                # print(repr([x, "%.10f" % percentHuman, "%.10f" % percentBacVir]))
                writer.writerow([x, "%.10f" % percentHuman, "%.10f" % percentBacVir])


def writeFileMappingDistributionJSON(dict, outfile):
    outputData = []

    outfile = open(outfile, 'w+')
    for x in dict:
        if not isinstance(dict[x][1], str):
            totalNumReads = float(dict[x][1])
            totalHumanReads = float(dict[x][3]) + float(dict[x][4])
            totalNonHumanReads = float(dict[x][2])
            percentBacVir = (float(totalNonHumanReads / totalNumReads) * 100)
            percentHuman = (float(totalHumanReads / totalNumReads) * 100)

            x = x.rstrip('\n')

            rowData = {}
            rowData["File"] = x
            rowData["Human"] = float("%.10f" % percentHuman)
            rowData["Non-Human"] = float("%.10f" % percentBacVir)

            outputData.append(rowData)

    outfile.write(json.dumps(outputData))


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
            ['Filename', '# of High Quality Blast Hits'])
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


def writeEMALGraphInfoJSON(infile, outfile):
    outfile = open(outfile, 'w+')

    outputData = []

    with open(infile, newline='') as inputFile:
        for line in inputFile:
            reader = csv.reader(inputFile, delimiter=',', quotechar='"')
            for row in reader:
                rowData = {}
                string = row[2].split('[')[0] + '=' + row[3].split('[')[0] + '=' + row[4].split('[')[0] + '=' + \
                         row[5].split('[')[0] + '=' + row[6].split('[')[0] + '=' + row[7].split('[')[0] + '=' + \
                         row[1].split('[')[0]
                rowData["Taxonomy"] = string
                rowData["GRA"] = row[0]

                outputData.append(rowData)

    outfile.write(json.dumps(outputData))
    outfile.close()


# Will determine which data is related to the category that should be summed over
def gatherSummedOverInfo(list, category):
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
                if x[0] != 'GRA':
                    dict[key] = float(x[0])

    return dict


def writeSummedOverInfo(category, dict, outfile):
    with open(outfile, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['GRA', category.rstrip()])
        for key in dict:
            writer.writerow([dict[key], key.strip('\n')])
        csvfile.close()


def writeSummedOverInfoJSON(category, dict, outfile):
    outfile = open(outfile, 'w+')
    allData = []

    for key in dict:
        rowData = {}

        rowData["GRA"] = dict[key]
        rowData[category.strip('\n')] = key.strip('\n')

        allData.append(rowData)

    outfile.write(json.dumps(allData))

def getAllTaxInfo (taxIDs):
    Entrez.email = "pkczeczk@ucalgary.ca"
    search_results = Entrez.read(Entrez.efetch("taxonomy", id=",".join(taxIDs)))
    allTaxInfo = {}

    for i in range(0, len(search_results)):
        taxonomicInfo = search_results[i]

        # Pull relevant information about that virus
        taxid = taxonomicInfo['TaxId']
        lineage = taxonomicInfo['LineageEx']
        species = taxonomicInfo['ScientificName']

        lineage[1]['Rank'] = 'Q1'

        allTaxInfo[taxid] = {'lineage': lineage, 'species': species}

    return allTaxInfo

def calculateActualAbunbdance(taxonomyLevels, projName, projDir, outputDirectory):
    if not projDir.endswith('/'):
        projDir = projDir + '/'

    fileDIR = projDir + '4-OrganismMapping/'
    combGenomeData = projDir + '5-RelativeAbundanceEstimation/'+projName+'-combinedGenomeData.csv'
    genomeTaxon = {}
    results = {}

    # Get all of the taxonomic ids in the set
    inputFile = open(combGenomeData, "r")
    for line in inputFile:
        genomeID, taxonID, genomeLen = line.split(',')
        genomeTaxon[int(genomeID)] = [int(taxonID), int(genomeLen)]

    # Get all taxonomic information for those IDs from ENTREZ
    allTaxIDS = []
    for key in genomeTaxon.keys():
        allTaxIDS.append(str(genomeTaxon[key][0]))

    allTaxInfo = getAllTaxInfo(allTaxIDS)

    for taxLevel in taxonomyLevels:
        results[taxLevel.upper()] = {}

    # process each blast result file
    for file in os.listdir(fileDIR):
        if '.tsv' in file:
            with open(fileDIR + file) as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for row in reader:
                    nucID = int(row[1].split('|')[1])

                    # Convert that reads nucID to its taxID
                    if nucID in genomeTaxon:
                        taxID = str(genomeTaxon[nucID][0])

                        for data in allTaxInfo[taxID]['lineage']:
                            taxLevel = data['Rank'].upper()
                            name = data['ScientificName'] + ' [' + data['TaxId'] + ']'

                            #Check if that name is already in results
                            if taxLevel in results:
                                if name in results[taxLevel]:
                                    results[taxLevel][name] += 1
                                else:
                                    results[taxLevel][name] = 1

    for level in results:
        with open(outputDirectory+'actualAbundanceSummedOver'+level+'.csv', 'w+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            writer.writerow([level,'# Reads Mapped'])

            for virus in results[level]:
                writer.writerow([virus,results[level][virus]])

if __name__ == "__main__":
    # Get the name of the project directory containing all of the results files
    projDir = sys.argv[1]
    projName = sys.argv[2]

    # Ensure the project directory ends with '/'
    if not projDir.endswith('/'):
        projDir += '/'

    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')
    configOptions = checkForExtraOptions(cwd + 'config.txt')

    createProjectInfoFile(projName, projDir)
    print('Gathering Step 1 Results...')
    prinseqInfo = getPRINSEQResults(projDir + '1-Cleaning/')
    writePrinseqTableFile(prinseqInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'prinseq-tbl-1.csv')
    print('Gathering Step 2 Results...')
    bowtieInfo = getBowtie2Results(projDir + '2-HumanMapping/')
    writeBowtieTableFile(bowtieInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'bowtie2-tbl-1.csv')

    writeFileMappingDistributionJSON(bowtieInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'mappedto.json')

    writeFileMappingDistribution(bowtieInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'mappedto.csv')
    print('Gathering Step 3 Results...')
    samtoolsInfo = getSamtoolsResults(projDir + '3-UnmappedCollection/')
    writeSamtoolsTable(samtoolsInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'samtools-tbl-1.csv')
    print('Gathering Step 4 Results...')
    blastInfo = gatherBlastResults(projDir + '4-OrganismMapping/')
    writeBlastTable(blastInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'blastn-tbl-1.csv')
    print('Gathering Step 5 Results...')
    emalInfo = gatherEMALResults(projDir + '5-RelativeAbundanceEstimation/')

    # Get list of all taxonomic levels considered
    taxonomyLevels = emalInfo[0]

    writeEMALTable(emalInfo, projDir + '6-FinalResult-'+projName+'/information/' + 'emal-tbl-1.csv')
    writeEMALGraphInfo(projDir + '6-FinalResult-'+projName+'/information/' + 'emal-tbl-1.csv',
                       projDir + '6-FinalResult-'+projName+'/information/' + 'emal-graph-1.csv')
    writeEMALGraphInfoJSON(projDir + '6-FinalResult-'+projName+'/information/' + 'emal-tbl-1.csv',
                           projDir + '6-FinalResult-'+projName+'/information/' + 'emal-graph-1.json')

    # Generate single summed over table
    summedOverResults = gatherSummedOverInfo(emalInfo, configOptions['extraTableSummedOver'].rstrip())
    writeSummedOverInfo(configOptions['extraTableSummedOver'], summedOverResults,
                        projDir + '6-FinalResult-'+projName+'/information/' + 'emal-tbl-2.csv')
    writeSummedOverInfoJSON(configOptions['extraTableSummedOver'], summedOverResults,
                            projDir + '6-FinalResult-'+projName+'/information/' + 'emal-tbl-2.json')

    # # Generate extra files that sum over each taxonomic level
    for x in taxonomyLevels:
        emalInfo.insert(0, taxonomyLevels)
        summedOverResults = gatherSummedOverInfo(emalInfo, x.rstrip())
        writeSummedOverInfo(x, summedOverResults, projDir + '6-FinalResult-'+projName+'/information/' + 'summedOver-' + x + '.csv')

    calculateActualAbunbdance(taxonomyLevels, projName, projDir, projDir + '6-FinalResult-'+projName+'/information/')

    print('Saving all csv files...')
    print('Complete!')
