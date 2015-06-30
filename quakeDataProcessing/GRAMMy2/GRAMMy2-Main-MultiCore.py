__author__ = 'patrickczeczko'

# Required Modules
import os
import argparse
import multiprocessing as mp
import time

BLASTFileDir = "/Users/patrickczeczko/GithubRepos/viral-metagen/quakeData/BLASTResults/MPT1.75/"
BLASTFileArray = []

outputFileName = ""

information = {}
pi = []
pMatrix = []
totalNumberOfReads = 0
numberOfThreads = 1

verbose = True

# Allow for command line arguments to be set and parsed
def parseCommandLineArguments ():
    global BLASTFileDir
    global verbose
    global numberOfThreads
    global outputFileName

    parser = argparse.ArgumentParser()

    #Required Arguments
    parser.add_argument("-d","--directory", type=str, required=True,
                        help="Provide a complete path to a direcotry containing the files of interest")

    #Optional Arguments
    parser.add_argument("-v", "--verbose", action="store_true" ,
                        help="Outline steps of the program as they occur")
    parser.add_argument("-t","--threads", type=int,
                        help="Number of concurrent threads to run. Default value is 1")
    parser.add_argument("-c","--csvname", type=str,
                        help="Indicate a filename for the file output csv to be written to. Default: output.csv")

    args = parser.parse_args()

    # Set arguments
    BLASTFileDir = args.directory
    if not BLASTFileDir.endswith("/"):
        BLASTFileDir+='/'
    if args.threads is not None:
        numberOfThreads = args.threads
    if args.csvname is not None:
        outputFileName = args.csvname
    if args.verbose:
        verbose = True


# Generate a list of all files to be processed
def getBlastFileList (fileDir):
    for file in os.listdir(fileDir):
        BLASTFileArray.append(fileDir+file)

# Create a dictionary that contains relevant information about each sample
# Each value within the dictionary is a list containing the following information
#   0: NCBI Nucleotide ID
#   1: NCBI Taxonomy ID
#   2: Length of Corresponding Genome
#   3: Index in pi array
def initializeInformation (information):
    inputFile = open("combinedGenomeData.csv","r")
    for line in inputFile:
        genomeID, taxonID, genomeLen, other = line.split(',')

        if genomeID in information:
            list = information[genomeID]
            list [1] = taxonID
            list [2] = genomeLen
            information[genomeID] = list

# Gather important initial information from the read files
def processBLASTFiles (fileList):
    totalNumberOfReads = 0
    for file in fileList:
        with open(file,'r') as inFile:
            for line in inFile:
                linePar = line.split('\t')
                genomeID = linePar[1].split('|')[1]
                list = [genomeID,0,0,0,0]
                information[genomeID] = list
                totalNumberOfReads += 1
    return information, totalNumberOfReads

# Create the pi vecotr that will store the probabilities throughout the process
def makePiVectorIndicies (information):
    list = []
    for x in information:
        list.append(x)
    list.sort()
    for x in list:
        information[x][3] = list.index(x)
    vector = [0] * len(list)
    return information, vector

def processOnefile (file,outputQ):
    inputFile = open(file,'r')
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
def initializePiVector (fileList,totalNumberOfReads):
    global numberOfThreads
    pool = mp.Pool(numberOfThreads)
    m = mp.Manager()
    outputQ = m.Queue()

    results=[]

    for file in fileList:
        proc = pool.apply_async(processOnefile, args=[file, outputQ])
        results.append(proc)

    pool.close()
    pool.join()

    while not outputQ.empty():
        piRow = outputQ.get()
        for i in range(len(piRow)):
            pi[i] += piRow[i]

    return pi, totalNumberOfReads

# Goes through and standardizes the pi vector after it has been set
def standardizeVector(vector):
    total = 0
    for x in vector:
        total += x
    for i in range(len(vector)):
        vector[i] = float(vector[i])/total
    return vector

# Creates the initial PMatrix
def initializePmatrix(numOfGenomes,numOfReads,fileList):
    columnHead = [0 for col in range(numOfGenomes)]
    columnHead[0] = 'ID'

    matrix = [[0 for col in range(numOfGenomes)] for row in range(numOfReads)]
    matrix[0] = columnHead

    for file in fileList:
        oFile = open(file)
        for i,line in enumerate(oFile):
            i += 1
            parse = line.split('\t')
            readID = parse[0]
            genomeID = parse[1].split('|')[1]
            columnIndex = information[str(genomeID)][3]+1

            matrix[i][0] = readID
            matrix[i][columnIndex] += 1
            if matrix[0][columnIndex] == 0:
                matrix[0][columnIndex] = genomeID

    return matrix

def initializePDictionary (numOfGenomes,numOfReads,fileList,information):
    pDiction = {}

    for file in fileList:
        oFile = open(file)
        for i,line in enumerate(oFile):
            parse = line.split('\t')
            readID = parse[0]
            genomeID = parse[1].split('|')[1]
            try:
                genomeLength = int(information[genomeID][2])
                if not readID in pDiction:
                    pDiction[readID] = [[genomeID,(1/genomeLength)]]
                else:
                    list = pDiction[readID]
                    list.append([genomeID,(1/genomeLength)])
                    pDiction[readID] = list
            except:
                print('Missing Genome Information :'+str(genomeID))

    return pDiction

def standardizePDictionary (pDiction):
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

def standardizeMatrixByColumn(matrix):
    for j in range(1,len(matrix[0])):
        sum = 0
        for i in range(1,len(matrix)):
            sum += matrix[i][j]
        if sum > 0:
            for i in range(1,len(matrix)):
                value = matrix[i][j]
                matrix[i][j] = float(value)/sum
    return matrix

def calculateZRow (mappedRead,numOfGenomes,pi,outputQ,information):
    zRow = [0.0 for col in range(numOfGenomes)]

    for loci in mappedRead:
        genomeID = loci[0]
        genomeIndex = information[genomeID][3]
        pValue = loci[1]
        piValue = pi[genomeIndex]

        zRow[genomeIndex] = pValue * piValue

    sumOfRow = sum(zRow)
    for j in range(len(zRow)):
        zRow[j] = zRow[j]/sumOfRow

    outputQ.put(zRow)

def eStep (pDiction,pi,cpu_count,information):
    pool = mp.Pool(cpu_count)
    m = mp.Manager()
    outputQ = m.Queue()

    results=[]

    for i in pDiction:
        mappedRead = pDiction[i]
        proc = pool.apply_async(calculateZRow,args=[mappedRead,len(pi),pi,outputQ,information])
        results.append(proc)

    pool.close()
    pool.join()

    return outputQ

def mStep (pi,outputQ):
    newPi = [0.0]*len(pi)

    tNR = 0
    while not outputQ.empty():
        zRow = outputQ.get()
        for i in range(len(zRow)):
            newPi[i] += zRow[i]
        tNR += 1
    for j in range(len(pi)):
        pi[j] = newPi[j]/tNR

    return pi

def outputCSV (information,pi):
    global outputFileName
    print(outputFileName)

    print(os.getcwd())
    outputFile = open(os.getcwd()+'/'+outputFileName,'w+')

    genomeIDs = ["GenomeID"]
    taxonIDs = ["TaxonID"]
    abundances = ["Relative Abundancies"]

    # Places all abundancies in the correct locations
    for x in pi:
        abundances.append(x)
        genomeIDs.append(0)
        taxonIDs.append(0)

    for x in information:
        index = information[x][3]+1
        genomeIDs[index] = information[x][0]
        taxonIDs[index] = information[x][1]

    csv = []

    for i in range (0,len(genomeIDs)):
        csv.append([genomeIDs[i],taxonIDs[i],abundances[i]])

    for i in range(0,len(csv)):
        for j in range (0,len(csv[i])):
            outputFile.write(str(csv[i][j])+',')
        outputFile.write('\n')

if __name__ == '__main__':
    parseCommandLineArguments()
    if verbose == True:
        print("\nGRAMMy2 0.1b \n")

        print("Grabbing list of files to process from:\n"+BLASTFileDir)
        getBlastFileList(BLASTFileDir)

        print("Preparing to run...")
        information, totalNumberOfReads = processBLASTFiles(BLASTFileArray)

        print("Starting run...")
        print("1. Calulating PiVector...")
        information, pi = makePiVectorIndicies(information)
        pi, totalNumberOfReads = initializePiVector(BLASTFileArray,totalNumberOfReads)
        pi = standardizeVector(pi)

        print("2.Gathering information...")
        initializeInformation(information)

        print("3.Initialzing PMatrix...")
        pDiction = initializePDictionary(len(pi)+1,totalNumberOfReads+1,BLASTFileArray,information)
        pDiction = standardizePDictionary(pDiction)

        print("4.Starting Abundance Calculation...")
        print("This could take a while perhaps you would like to grab a beverage...")

        start = time.time()
        previousPi = pi
        outputQ = eStep(pDiction,pi,numberOfThreads,information)
        pi = mStep(pi,outputQ)

        while pi != previousPi:
            previousPi = pi
            outputQ = eStep(pDiction,pi,numberOfThreads,information)
            pi = mStep(pi,outputQ)
        end = time.time()

        print("Abundance Calculations took: "+str(end-start))
        print("5. Calculation Complete!")
        print("6. Printing results in CSV format!")
        outputCSV(information,pi)
        print("Exiting...")
    else:
        print("\nGRAMMy2 0.1b\n")

        getBlastFileList(BLASTFileDir)

        information, totalNumberOfReads = processBLASTFiles(BLASTFileArray)

        information, pi = makePiVectorIndicies(information)
        pi, totalNumberOfReads = initializePiVector(BLASTFileArray,totalNumberOfReads)
        pi = standardizeVector(pi)

        initializeInformation(information)

        pDiction = initializePDictionary(len(pi)+1,totalNumberOfReads+1,BLASTFileArray,information)
        pDiction = standardizePDictionary(pDiction)

        previousPi = pi
        outputQ = eStep(pDiction,pi,numberOfThreads,information)
        pi = mStep(pi,outputQ)
        outputQ.queue.clear()
        while pi != previousPi:
            previousPi = pi
            outputQ = eStep(pDiction,pi,numberOfThreads,information)
            pi = mStep(pi,outputQ)
            outputQ.queue.clear()
        outputCSV(information,pi)
        print("Exiting...")
