# =================================================
# EMAL-Main
# Version: 1.0
#
# Author: Patrick Czeczko
# Made at: de Koning Lab
# Link: http://lab.jasondk.io
# Github:
#
# Documentation can be found on the github page.
# =================================================

# Required Modules
import os
import random
import string
import argparse
import multiprocessing as mp
import time
import math
from functools import reduce

# Global information
BLASTFileDir = ""
BLASTFileArray = []

# Output file names
outputFileName = "output-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) + ".csv"
logfile = ''
outputDir = os.getcwd() + '/'
combinedGenomeDataFile = ''

information = {}
pi = []
pMatrix = []
genomeTaxon = {}
totalNumberOfReads = 0  # sij
totalGenomeSizes = 0

# Command Line Options
numberOfThreads = 4
acceptanceValue = 0.0001
verbose = False
fileExtension = '.tsv'


# Allow for command line arguments to be set and parsed
def parseCommandLineArguments():
    global BLASTFileDir
    global verbose
    global numberOfThreads
    global outputFileName
    global acceptanceValue
    global fileExtension
    global combinedGenomeDataFile

    # Creates argument parser instance
    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="Provide a complete path to a directory containing the files of interest")
    parser.add_argument("-i", "--combinedGenomeData", type=str, required=True,
                        help="Full path to the result file from EMAL-DataPrep")

    # Optional Arguments
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Outline steps of the program as they occur")
    parser.add_argument("-t", "--threads", type=int,
                        help="Number of concurrent threads to run. Default value is 1")
    parser.add_argument("-c", "--csvname", type=str,
                        help="Indicate a filename for the file output csv to be written to. Default: output.csv")
    parser.add_argument("-m", "--maximumLikelihoodConvergenceCriterion", type=float,
                        help="Indicate the acceptable difference within the range of this number. Default: 0.0001")
    parser.add_argument("-o", "--outputdir", type=str,
                        help="Path to a directory where output should be placed")
    parser.add_argument("-e", "--fileext", type=str,
                        help="file extension of blast results")

    args = parser.parse_args()

    # Set arguments
    BLASTFileDir = args.directory
    combinedGenomeDataFile = args.combinedGenomeData

    if not BLASTFileDir.endswith("/"):
        BLASTFileDir += '/'
    if args.threads is not None:
        numberOfThreads = args.threads
    if args.csvname is not None:
        outputFileName = args.csvname
    if args.verbose:
        verbose = True
    if args.maximumLikelihoodConvergenceCriterion is not None:
        acceptanceValue = args.maximumLikelihoodConvergenceCriterion
    if args.outputdir is not None:
        outputDir = args.outputdir
        if not outputDir.endswith('/'):
            outputDir += '/'
    if args.fileext is not None:
        fileExtension = args.fileext


# Generate a list of all files within the BLASTFileDir to be processed.
# Checks each file for the presence of BLAST results to prevent blank
# file processing.
def getBlastFileList(fileDir):
    global fileExtension
    for file in os.listdir(fileDir):
        if fileExtension is not None:
            if file.endswith(fileExtension):
                if checkForEmptyFile(fileDir + file):
                    BLASTFileArray.append(fileDir + file)
        else:
            BLASTFileArray.append(fileDir + file)


# Check to see if file contains any tabular information that
# should be present within file for appropriate processing
def checkForEmptyFile(path):
    openFile = open(path, 'r')
    firstLine = openFile.readline()
    if '\t' in firstLine:
        return True
    else:
        return False


# Gathers initial information about genomes to be evaluated
def gatherInformation(fileList):
    global totalGenomeSizes
    global combinedGenomeDataFile

    totalNumberOfReads = 0

    # Dictionary to contain all pertinent information about genomes
    # including basic taxonomic identification number
    information = {}

    # Dictionary Containing Information of how many times a read maps to each genome
    blastHits = {}

    # Create Nucleotide ID and Taxonomy ID associations
    inputFile = open(combinedGenomeDataFile, "r")
    for line in inputFile:
        genomeID, taxonID, genomeLen = line.split(',')
        genomeLen = genomeLen.strip('\n')
        genomeTaxon[int(genomeID)] = [int(taxonID), int(genomeLen)]

    # Gather information on files present within set to be analyzed
    for file in fileList:
        with open(file, 'r') as inFile:
            for read in inFile:
                linePar = read.split('\t')

                genomeID = int(linePar[1].split('|')[1])
                readID = linePar[0]

                try:
                    taxonID = genomeTaxon[genomeID][0]  # The taxonID for the read from that line in the blast file
                    genomeLen = int(genomeTaxon[genomeID][1])  # The length of the genome for that read

                    # totalGenomeSizes += genomeLen
                    totalNumberOfReads += 1

                    if genomeID not in information:
                        information[genomeID] = [genomeID, taxonID, genomeLen, 0]

                    # Read is already in the blast hits. AKA the read maps to multiple genomes
                    if readID in blastHits:
                        blastHits[readID][genomeID] = 1

                    # Read is completely new
                    else:
                        blastHits[readID] = {}
                        blastHits[readID][genomeID] = 1

                except:
                    missing = genomeID

    logfile.write("Total number of reads that match taxon information: " + str(totalNumberOfReads) + '\n')

    return information, genomeTaxon, totalNumberOfReads, blastHits  # Create a list to be used to store the pi values


# Creates the pi vector and notes the index values of each genome in information
def makePiVectorIndicies(information):
    list = []
    for x in information:
        list.append(x)
    list.sort()
    for x in list:
        information[x][3] = list.index(x)
    vector = [0.0 for col in range(len(list))]
    return information, vector


# Initialize pi vector to number of reads in genome over the total reads in set
def initializePiVector(blastHits, information, piVector):
    for read in blastHits:
        for genomeMappedToRead in blastHits[read]:
            piIndex = information[genomeMappedToRead][3]
            piVector[piIndex] += 1

    piVectorStandardized = standardizeVector(piVector)

    return piVectorStandardized


# Standardizes a list of values
def standardizeVector(vector):
    total = 0
    for x in vector:
        total += x
    for i in range(len(vector)):
        vector[i] = float(vector[i]) / total
    return vector


# Calculate sij/lj
def calculateHitsOverLength(blastHits, information):
    sijOverlj = {}

    for read in blastHits:
        if read not in sijOverlj:
            sijOverlj[read] = {}

        for genomeMapped in blastHits[read]:
            sijOverlj[read][genomeMapped] = blastHits[read][genomeMapped] / genomeTaxon[genomeMapped][1]

    return sijOverlj


# Calculate Zij
def eStep(blastHits, sijOverlj, piVector):
    z = {}  # Dictionary with all zij vlaues

    for read in blastHits:  # Zi
        # if the read is not in z yet add a dictionary to hold data
        if read not in z:
            z[read] = {}

        # for each genome in the blast hits for that read
        for genomeMapped in blastHits[read]:  # Zij
            # determine the pi value at time t for that that genome
            piIndex = information[genomeMapped][3]
            piValue = piVector[piIndex]  # pij at time t

            # determine the sij/lj value for that read at that genome
            sijOverljValue = sijOverlj[read][genomeMapped]

            # determine sum of sik/lk for all genomes at that read
            sumsikoverlk = 0
            for genomeK in sijOverlj[read]:
                sumsikoverlk += (sijOverlj[read][genomeK] * piVector[information[genomeK][3]])

            # calculate zij = ((sij/lj)*pij)/(sum((sik/lk)*pik))
            z[read][genomeMapped] = (sijOverljValue * piValue) / (sumsikoverlk)

    return z


#
def mStep(z, oldPi):
    newPi = []

    for spot in oldPi:
        newPi.append(0.0)

    for read in z:  # Zi
        for genomej in z[read]:
            newPi[information[genomej][3]] += z[read][genomej]

    for genomeJ in information:
        newPi[information[genomeJ][3]] = newPi[information[genomeJ][3]] / totalNumberOfReads

    newPi = standardizeVector(newPi)

    return newPi


# Compare each list and determine if the differences in value as small enough
# between iterations to accept result
def compareLists(old, new, acceptance):
    global logfile
    diff = []
    accept = True

    print(old)
    print(new)

    for i in range(len(old)):
        diff.append(abs(old[i] - new[i]))
    for i in diff:
        if i > acceptance:
            accept = False
    logfile.write(str(old) + '\n')
    logfile.write(str(new) + '\n')
    logfile.write(str(diff) + '\n')
    return accept


def calculateGenomeRelativeAbundacies(finalPi):
    abundancies = []

    for genomeJ in information:
        abundancies.append(0)

    sumPiKoverLk = 0
    for genomeK in information:
        piK = finalPi[information[genomeK][3]]
        lK = information[genomeK][2]

        sumPiKoverLk += (piK / lK)

    for genomeJ in information:
        piJ = finalPi[information[genomeJ][3]]
        lenJ = information[genomeJ][2]

        abundancies[information[genomeJ][3]] = (piJ) / ((lenJ) * (sumPiKoverLk))

    return abundancies


# This function writes the results to a CSV file.
# Format (Columns):
#   1: NCBI Nucleotide ID
#   2: NCBI Taxonomy ID
#   3: Relative Abundance for that genome
def outputCSV(information, gra):
    global outputFileName

    outputFile = open(outputDir + outputFileName, 'w+')

    genomeIDs = ["GenomeID"]
    taxonIDs = ["TaxonID"]
    abundances = ["Relative Abundancies"]

    # Places all abundances in the correct locations
    for x in gra:
        abundances.append(x)
        genomeIDs.append(0)
        taxonIDs.append(0)

    for x in information:
        index = information[x][3] + 1
        genomeIDs[index] = information[x][0]
        taxonIDs[index] = information[x][1]

    csv = []

    for i in range(0, len(genomeIDs)):
        csv.append([genomeIDs[i], taxonIDs[i], abundances[i]])

    for i in range(0, len(csv)):
        for j in range(0, len(csv[i])):
            outputFile.write(str(csv[i][j]) + ',')
        outputFile.write('\n')


# Main Function
if __name__ == '__main__':
    print("\nEMAL 0.2b \n")
    # Parse command line arguments to ensure correct process occurs
    parseCommandLineArguments()

    # Create log file
    logfile = open(outputDir + 'EMALLog-' + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) + '.txt', 'w+')
    logfile.write('Analysis on files within:' + BLASTFileDir)

    if verbose:
        print("Number of Threads: " + str(numberOfThreads))
        print("Acceptance Value: " + str(acceptanceValue))
        print("Grabbing list of files to process from:\n" + BLASTFileDir)

    # Get all files in the directory specified
    getBlastFileList(BLASTFileDir)

    if verbose:
        print(str(len(BLASTFileArray)) + " files found to process:")
        for x in BLASTFileArray:
            print(x)

    # if there are files to process
    if len(BLASTFileArray) > 0:
        if verbose:
            print("Preparing to run...")

        # Determine necessary initial information
        information, genomeTaxon, totalNumberOfReads, blastHits = gatherInformation(BLASTFileArray)

        if verbose:
            print("Starting run...")
            print("1. Calculating Initial PiVector...")

        # Calculate initial values for Pi Vector
        information, pi = makePiVectorIndicies(information)
        pi = initializePiVector(blastHits, information, pi)

        count = 0  # number of cycles
        if verbose:
            print("2. Calculating Zij...")
        start = time.time()  # Grab the start time

        sijOverlj = calculateHitsOverLength(blastHits, information)
        z = eStep(blastHits, sijOverlj, pi)

        oldPi = pi

        if verbose:
            print("3. Calculating revised pi values...")
        newPi = mStep(z, oldPi)
        count += 1

        if verbose:
            print('\t' + str(count) + ' Cycles completed')

        accept = compareLists(oldPi, newPi, acceptanceValue)

        while accept == False:
            oldPi = newPi
            z = eStep(blastHits, sijOverlj, oldPi)
            newPi = mStep(z, oldPi)
            count += 1
            if verbose:
                print('\t' + str(count) + ' Cycles completed')
            accept = compareLists(oldPi, newPi, acceptanceValue)

        end = time.time()  # Grab the end time
        if verbose:
            print("4. Calculating final GRA values...")
        gra = calculateGenomeRelativeAbundacies(newPi)

        if verbose:
            print("Abundance Calculations took: " + str(end - start)+ " sec")
            print("Values calculated in " + str(count) + " cycles!")
            print("Final GRA:")
            print(gra)

        # Complete process and output relevant information to CSV file
        outputCSV(information, gra)

        print("Calculations completed successfully!")
        print("Exiting...")

    else:
        print('No files found to process')
