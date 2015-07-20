__author__ = 'patrickczeczko'

# Required Modules
import os
import argparse
import multiprocessing as mp
import time

BLASTFileDir = "/Users/patrickczeczko/GithubRepos/viral-metagen/quakeDataProcessing/EMAL-Validation/"
#BLASTFileArray = [BLASTFileDir + 'newDataDuplicateMappings.tblat']
BLASTFileArray = []

outputFileName = "output2.csv"

information = {}
pi = []
pMatrix = []
totalNumberOfReads = 0
totalGenomeSizes = 0

# Command Line Options
numberOfThreads = 1
acceptanceValue = 0.0001
verbose = True

# Allow for command line arguments to be set and parsed
def parseCommandLineArguments():
    global BLASTFileDir
    global verbose
    global numberOfThreads
    global outputFileName
    global acceptanceValue

    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="Provide a complete path to a directory containing the files of interest")

    # Optional Arguments
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Outline steps of the program as they occur")
    parser.add_argument("-t", "--threads", type=int,
                        help="Number of concurrent threads to run. Default value is 1")
    parser.add_argument("-c", "--csvname", type=str,
                        help="Indicate a filename for the file output csv to be written to. Default: output.csv")
    parser.add_argument("-a", "--acceptanceCutoff", type=float,
                        help="Indicate the acceptable difference with range of this numebr. Default: 0.1")
    args = parser.parse_args()

    # Set arguments
    BLASTFileDir = args.directory
    if not BLASTFileDir.endswith("/"):
        BLASTFileDir += '/'
    if args.threads is not None:
        numberOfThreads = args.threads
    if args.csvname is not None:
        outputFileName = args.csvname
    if args.verbose:
        verbose = True
    if args.acceptanceCutoff is not None:
        acceptanceValue = args.acceptanceCutoff


# Generate a list of all files within the BLASTFileDir to be processed
def getBlastFileList(fileDir):
    for file in os.listdir(fileDir):
        BLASTFileArray.append(fileDir + file)


# Gather important initial information from the read files
# - NCBI Nucleotide IDs
# - Total Number of Reads within all files
def processBLASTFiles(fileList):
    totalNumberOfReads = 0
    for file in fileList:
        with open(file, 'r') as inFile:
            for line in inFile:
                linePar = line.split('\t')
                genomeID = linePar[1].split('|')[1]
                list = [genomeID, 0, 0, 0, 0]
                information[genomeID] = list
                totalNumberOfReads += 1
    return information, totalNumberOfReads


# Create a list to be used to store the pi values
def makePiVectorIndicies(information):
    list = []
    for x in information:
        list.append(x)
    list.sort()
    for x in list:
        information[x][3] = list.index(x)
    vector = [0] * len(list)
    return information, vector


# Processes one file to initalize the Pi vector
# Returns a list which is placed into the output queue
def processOnefile(info):
    file = info[0]
    outputQ = info[1]

    inputFile = open(file, 'r')
    for line in inputFile:
        linePar = line.split('\t')
        genomeID = linePar[1].split('|')[1]
        try:
            piIndex = information[str(genomeID)][3]
            pi[piIndex] += 1
        except:
            # print(',')
            print('Missing information for Id: ' + genomeID)
    outputQ.put(pi)


# Goes through each file in the directory and reads the number of blast hits in each file
# Each blast hit adds 1 to the corresponding pi matrix location
def initializePiVector(fileList, totalNumberOfReads):
    global numberOfThreads
    pool = mp.Pool(numberOfThreads)
    m = mp.Manager()
    outputQ = m.Queue()

    iterInfo = []

    for file in fileList:
        print (file)
        iterInfo.append([file, outputQ])

    proc = pool.map_async(processOnefile, iterInfo)

    pool.close()
    pool.join()

    while not outputQ.empty():
        piRow = outputQ.get()
        for i in range(len(piRow)):
            pi[i] += piRow[i]

    return pi, totalNumberOfReads

# Standardizes a list of values
def standardizeVector(vector):
    total = 0
    for x in vector:
        total += x
    for i in range(len(vector)):
        vector[i] = float(vector[i]) / total
    return vector

# Create a dictionary that contains relevant information about each sample
# Each value within the dictionary is a list containing the following information
#   0: NCBI Nucleotide ID
#   1: NCBI Taxonomy ID
#   2: Length of Corresponding Genome
#   3: Index in pi array
def initializeInformation(information):
    global totalGenomeSizes

    inputFile = open("combinedGenomeData.csv", "r")
    for line in inputFile:
        genomeID, taxonID, genomeLen = line.split(',')

        if genomeID in information:
            list = information[genomeID]
            list[1] = taxonID
            list[2] = genomeLen
            totalGenomeSizes += int(genomeLen)
            information[genomeID] = list


# Initializes a dictionary filled with Maximum Likelihood Estimates (MLE)
#   - Key: readID (Identifier found in 1st Column of Tabular blastn output)
#   - Values: [[NCBI NucleotideID, MLE]...]
def initializePDictionary(numOfGenomes, numOfReads, fileList, information):
    pDiction = {}

    for file in fileList:
        oFile = open(file)
        for i, line in enumerate(oFile):
            parse = line.split('\t')
            readID = parse[0]
            genomeID = parse[1].split('|')[1]
            try:
                genomeLength = int(information[genomeID][2])
                if not readID in pDiction:
                    pDiction[readID] = [[genomeID, (1 / genomeLength)]]
                else:
                    list = pDiction[readID]
                    list.append([genomeID, (1 / genomeLength)])
                    pDiction[readID] = list
            except:
                print('Missing Genome Information :' + str(genomeID))

    return pDiction


# Function will standardize the entire MLE dictionary by read
def standardizePDictionary(pDiction):
    for read in pDiction:
        mappedLoci = pDiction[read]
        sum = 0
        for x in mappedLoci:
            sum += x[1]
        updateDic = {}
        list = []
        for x in mappedLoci:
            list.append([x[0], (x[1] / sum)])
        updateDic[read] = list
        pDiction.update(updateDic)
    return pDiction


# Calculates a single row of posterior probabilities
# Results are placed in dictionaries to reduce the required
# amount of memory used for this algorithm
def calculateZRow(info):
    mappedRead = info[0]
    readID = info[1]
    pi2 = info[2]
    outputQ = info[3]
    information = info[4]

    zValues = {}

    for loci in mappedRead:
        genomeID = loci[0]
        genomeIndex = information[genomeID][3]
        pValue = loci[1]
        piValue = pi2[genomeIndex]
        z = (pValue * piValue)

        if not readID in zValues:
            zValues[readID] = [[genomeID, z]]
        else:
            list = zValues[readID]
            list.append([genomeID, z])
            zValues[readID] = list

    sumValue = 0
    zValueArray = zValues[readID]
    for i in zValueArray:
        sumValue += i[1]

    for i in range(len(zValueArray)):
        num = zValueArray[i][1]
        num = num / sumValue
        zValueArray[i][1] = num

    duplicates = {}
    finalArray = []

    for i in range(len(zValueArray)):
        if zValueArray[i][0] in duplicates:
            duplicates[zValueArray[i][0]] += zValueArray[i][1]
        else:
            duplicates[zValueArray[i][0]] = zValueArray[i][1]

    for i in duplicates:
        finalArray.append([str(i), duplicates[i]])

    zValues[readID] = finalArray

    outputQ.put(zValues)


# Runs the estimation step of the EM algorithm used.
# The process has been broken down so that each read can be processed by a
# single thread reducing the amount of time needed to achieve final viral
# abundances
def eStep(pDiction, pi2, cpu_count, information):
    pool = mp.Pool(cpu_count)
    m = mp.Manager()
    outputQ = m.Queue()

    iterbaleInformation = []
    for i in pDiction:
        mappedRead = pDiction[i]
        iterbaleInformation.append([mappedRead, i, pi2, outputQ, information])

    proc = pool.map_async(calculateZRow, iterbaleInformation)

    pool.close()
    pool.join()

    return outputQ


# Runs the maximization step of the EM algorithm used.
# This step essentially calculates new pi values from the results of the
# estimation step. These pi value are then used in the next iteration of
# the algorithm to determine relative abundances
def mStep(pi2, outputQ):
    global totalNumberOfReads, information, totalGenomeSizes
    newPi = [0.0 for col in range(len(pi2))]

    tNR = 0

    indexLength = {}
    for x in information:
        list = information[x]
        length = list[2]
        index = list[3]
        indexLength[index] = float(length)

    while not outputQ.empty():
        read = outputQ.get()
        tNR += 1
        for i in read:
            zijs = read[i]
            for x in zijs:
                genomeID = x[0]
                z = x[1]
                index = information[genomeID][3]
                newPi[index] += z

    for j in range(len(pi2)):
        newPi[j] = totalGenomeSizes * (newPi[j] / (tNR * indexLength[j]))

    # newPi = standardizeVector(newPi)

    return newPi


# This function writes the results to a CSV file.
# Format (Columns):
#   1: NCBI Nucleotide ID
#   2: NCBI Taxonomy ID
#   3: Relative Abundance for that genome
def outputCSV(information, pi):
    global outputFileName

    outputFile = open(os.getcwd() + '/' + outputFileName, 'w+')

    genomeIDs = ["GenomeID"]
    taxonIDs = ["TaxonID"]
    abundances = ["Relative Abundancies"]

    # Places all abundancies in the correct locations
    for x in pi:
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


# Compare each list and determine if the differences in value as small enough
# between iterations to accept result
def compareLists(old, new, acceptance):
    diff = []
    accept = True

    for i in range(len(old)):
        diff.append(abs(old[i] - new[i]))
    for i in diff:
        if i > acceptance:
            accept = False
    return accept

# Main Function
if __name__ == '__main__':
    # Parse command line arguments to ensure correct process occurs
    parseCommandLineArguments()
    if verbose:
        print("\nEMAL 0.2b \n")

        # Grab all files in the directory specified
        print("Grabbing list of files to process from:\n" + BLASTFileDir)
        getBlastFileList(BLASTFileDir)
        print(str(len(BLASTFileArray)) + " files found to process:")
        for x in BLASTFileArray:
            print(x)

        print("Preparing to run...")
        information, totalNumberOfReads = processBLASTFiles(BLASTFileArray)

        print("Starting run...")
        print("1. Calulating PiVector...")
        information, pi = makePiVectorIndicies(information)
        pi, totalNumberOfReads = initializePiVector(BLASTFileArray, totalNumberOfReads)
        pi = standardizeVector(pi)

        print("2.Gathering information...")
        initializeInformation(information)

        print("3.Initialzing MLEs...")
        pDiction = initializePDictionary(len(pi) + 1, totalNumberOfReads + 1, BLASTFileArray, information)
        pDiction = standardizePDictionary(pDiction)

        print("4.Starting Abundance Calculation...")
        print("This could take a while perhaps you would like to grab a beverage...")
        start = time.time()  # Grab the start time

        count = 0

        oldPi = pi
        outputQ = eStep(pDiction, pi, numberOfThreads, information)
        newPi = mStep(pi, outputQ)

        count += 1
        accept = compareLists(oldPi, newPi, acceptanceValue)

        while accept == False:
            oldPi = newPi
            outputQ = eStep(pDiction, newPi, numberOfThreads, information)
            newPi = mStep(newPi, outputQ)
            count += 1
            accept = compareLists(oldPi, newPi, acceptanceValue)
            print(str(count) + 'Cycles completed')

        newPi = standardizeVector(newPi)
        end = time.time()  # Grab the end time

        print("Abundance Calculations took: " + str(end - start))
        print("5. Calculation Complete! Took " + str(count) + " cycles")
        print("6. Printing results in CSV format!")
        outputCSV(information, newPi)
        print("Exiting...")
    else:
        print("\nEMAL 0.1b\n")

        getBlastFileList(BLASTFileDir)

        information, totalNumberOfReads = processBLASTFiles(BLASTFileArray)

        information, pi = makePiVectorIndicies(information)
        pi, totalNumberOfReads = initializePiVector(BLASTFileArray, totalNumberOfReads)
        pi = standardizeVector(pi)

        initializeInformation(information)

        pDiction = initializePDictionary(len(pi) + 1, totalNumberOfReads + 1, BLASTFileArray, information)
        pDiction = standardizePDictionary(pDiction)

        oldPi = pi
        outputQ = eStep(pDiction, pi, numberOfThreads, information)
        newPi = mStep(pi, outputQ)

        accept = compareLists(oldPi, newPi, acceptanceValue)
        while accept == False:
            oldPi = newPi
            outputQ = eStep(pDiction, newPi, numberOfThreads, information)
            newPi = mStep(newPi, outputQ)
            accept = compareLists(oldPi, newPi, acceptanceValue)

            outputQ.queue.clear()

        newPi = standardizeVector(newPi)
        outputCSV(information, newPi)
        print("Exiting...")
