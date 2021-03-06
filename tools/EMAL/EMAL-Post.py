# =================================================
# EMAL-Post
# Version: 1.0
#
# Author: Patrick Czeczko
# Made at: de Koning Lab
# Link: http://lab.jasondk.io
# Github:
#
# Documentation can be found on the github page.
# =================================================

from Bio import Entrez
import csv, os, sys
import multiprocessing as mp
import argparse

dataDic = {}
SKDic = {}
Q1Dic = {}
ODic = {}
FDic = {}
SBFDic = {}
GDic = {}

allTaxInfo = {}

inputFile = ''
outputFileName = 'output.csv'
outputDir = ''


# Allow for command line arguments to be set and parsed
def parseCommandLineArguments():
    global inputFile
    global outputFileName
    global outputDir

    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-f", "--file", type=str, required=True,
                        help="Provide a complete path to a file containing the output from EMAL-Main")
    parser.add_argument("-c", "--csvname", type=str,
                        help="Indicate a filename for the file output csv to be written to. Default: output.csv"
                             "Warning: if file already exists it will be over written")
    parser.add_argument("-o", "--outputdir", type=str,
                        help="Path to a directory where output should be placed")

    args = parser.parse_args()

    # Set arguments
    inputFile = args.file
    if args.csvname is not None:
        root, ext = os.path.splitext(args.csvname)
        if ext == '.csv':
            outputFileName = args.csvname
    if args.outputdir is not None:
        outputDir = args.outputdir
        if not outputDir.endswith('/'):
            outputDir += '/'


# Read in information from EMAL-Main output CSV
def processCSV(file):
    m = mp.Manager()
    outputQ = m.Queue()
    results = []

    # Get a list of all taxIDs found in the dataset
    taxIDS = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            taxIDS.append(row[1])
    taxIDS.pop(0)
    getAllTaxInfo(taxIDS)

    file = str(file)
    # Process through each result in the EMAL results
    inputFile = open(file, 'r')
    for i, line in enumerate(inputFile):
        if i != 0:
            processOneLine(line, outputQ)

    count = 0

    while not outputQ.empty():
        count += 1
        info = outputQ.get()
        if info[0] in dataDic:
            TaxID = info[0]
            GRA = float(info[1][0])
            GRA2 = float(dataDic[TaxID][0])
            GRATot = GRA + GRA2
            dataDic[TaxID][0] = GRATot

        else:
            dataDic[info[0]] = info[1]


def getAllTaxInfo(taxIDs):
    Entrez.email = "pkczeczk@ucalgary.ca"
    search_results = Entrez.read(Entrez.efetch("taxonomy", id=",".join(taxIDs)))

    for i in range(0, len(search_results)):
        taxonomicInfo = search_results[i]

        # Pull relevant information about that virus
        taxid = taxonomicInfo['TaxId']
        lineage = taxonomicInfo['LineageEx']
        species = taxonomicInfo['ScientificName']

        lineage[1]['Rank'] = 'Q1'
        for i in lineage:
            print(i)

        allTaxInfo[taxid] = {'LineageEx': lineage, 'ScientificName': species}


# Retrieve record from NCBI Entrez Data
def grabEntrezRecord(TaxID):
    return allTaxInfo[TaxID]['LineageEx'], allTaxInfo[TaxID]['ScientificName']


# Gather required information from Entrez Record
def processOneLine(line, outputQ):
    parse = line.split(',')
    TaxID = parse[1]

    lineage, species = grabEntrezRecord(TaxID)

    noRank = False

    superKingdom = ['Superkingdom', 'N/A', 'N/A']
    Q1 = ['Q1', 'N/A', 'N/A']
    Order = ['Order', 'N/A', 'N/A']
    Family = ['Family', 'N/A', 'N/A']
    SubFamily = ['SubFamily', 'N/A', 'N/A']
    Genus = ['Genus', 'N/A', 'N/A']

    for entry in lineage:
        if entry['Rank'] == 'superkingdom':
            superKingdom[1] = entry['ScientificName']
            superKingdom[2] = entry['TaxId']
            SKDic[superKingdom[2]] = superKingdom[1]
        elif entry['Rank'] == 'Q1':
            Q1[1] = entry['ScientificName']
            Q1[2] = entry['TaxId']
            Q1Dic[Q1[2]] = Q1[1]
        elif entry['Rank'] == 'order':
            Order[1] = entry['ScientificName']
            Order[2] = entry['TaxId']
            ODic[Order[2]] = Order[1]
        elif entry['Rank'] == 'family':
            Family[1] = entry['ScientificName']
            Family[2] = entry['TaxId']
            FDic[Family[2]] = Family[1]
        elif entry['Rank'] == 'subfamily':
            SubFamily[1] = entry['ScientificName']
            SubFamily[2] = entry['TaxId']
            SBFDic[SubFamily[2]] = SubFamily[1]
        elif entry['Rank'] == 'genus':
            Genus[1] = entry['ScientificName']
            Genus[2] = entry['TaxId']
            GDic[Genus[2]] = Genus[1]

    outputQ.put([TaxID, [parse[2], species, superKingdom, Q1, Order, Family, SubFamily, Genus]])


# Output all gathered information into a final CSV file
def createNewCSV(dataDic, outputFilename):
    with open(outputFilename, 'w+', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(('GRA', 'Species', 'SuperKingdom', 'Q1', 'Order', 'Family', 'SubFamily', 'Genus'))
        for i in dataDic:
            info = dataDic[i]

            for j in range(2,len(info)):
                if len(info[j]) > 1:
                    for k in range(len(info[j])):
                        if info[j][k] == None:
                            info[j][k] = 'N/A'

            info[3][1] = info[3][1].replace(',', '')

            writer.writerow((info[0], info[1] + ' [' + i + ']',
                             info[2][1] + ' [' + info[2][2] + ']',
                             info[3][1] + ' [' + info[3][2] + ']',
                             info[4][1] + ' [' + info[4][2] + ']',
                             info[5][1] + ' [' + info[5][2] + ']',
                             info[6][1] + ' [' + info[6][2] + ']',
                             info[7][1] + ' [' + info[7][2] + ']'))


# Main Function
if __name__ == '__main__':
    parseCommandLineArguments()
    print("Reading in information...")
    processCSV(inputFile)
    print('Creating new output file')
    createNewCSV(dataDic, outputDir + outputFileName)
    print('New CSV created')
