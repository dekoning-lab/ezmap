__author__ = 'patrickczeczko'

# Required Modules
import os
import argparse
import threading

BLASTFileDir = ""
BLASTFileArray = []

information = {}
pi = []
pMatrix = []
totalNumberOfReads = 0

verbose = False

def parseCommandLineArguments ():
    global BLASTFileDir
    global verbose

    parser = argparse.ArgumentParser()

    #Required Arguments
    parser.add_argument("d", "directory", help="Provide a complete path to a direcotry containing the files of interest")

    #Optional Arguments
    parser.add_argument("-v", "--verbose", help="Outline steps of the program as they occur, this will also provide a "
                                                "statment every 5 minutes when working on large datasets to ensure "
                                                "operations a stil occuring")
    args = parser.parse_args()

    BLASTFileDir  = args.directory
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

def makePiVectorIndicies (information):
    list = []
    for x in information:
        list.append(x)
    list.sort()
    for x in list:
        information[x][3] = list.index(x)
    vector = [0] * len(list)
    return information, vector

# Goes through each file in the directory and reads the number of blast hits in each file
# Each blast hit adds 1 to the corresponding pi matrix location
def initializePiVector (fileList,totalNumberOfReads):
    for file in fileList:
        inputFile = open(file,'r')
        for line in inputFile:
            linePar = line.split('\t')
            genomeID = linePar[1].split('|')[1]
            try:
                piIndex = information[str(genomeID)][3]
                pi[piIndex] += 1
            except:
                #print(',')
                print('Missing information for Id: '+genomeID)
    return pi, totalNumberOfReads

# Goes through and standardizes the pi vector after it has been set
def standardizeVector(vector):
    total = 0
    for x in vector:
        total += x
    for i in range(len(vector)):
        vector[i] = float(vector[i])/total
    return vector

def initializePmatrix(matrix,totalNumberOfReads,numOfCol,information,fileList):
    columnHead = [0] * numOfCol
    columnHead[0] = 'ID'
    for x in information:
        columnHead[information[x][3]+1] = x
    matrix.append(columnHead)

    for file in fileList:
        with open(file,'r') as inFile:
            for i,line in enumerate(inFile):
                linePar = line.split('\t')
                row = [0] * numOfCol
                row[0] = linePar[0]
                genomeID = linePar[1].split('|')[1]
                try:
                    index = information[str(genomeID)][3] + 1
                    row[index] += 1
                    matrix.append(row)
                except:
                    #print(',')
                    print('Missing information for Id: '+genomeID)

    return matrix

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

def eStep (pMatrix,pi):
    zMatrix = []
    cCol = 0

    for i in pMatrix:
        zRow = []
        if i[0] == 'ID':
            continue
        for j in i:
            if isinstance(j,str):
                continue
            p = j
            piValue = pi[cCol]
            z = p*piValue
            xCol = 0
            sValue = 0
            for x in i:
                if isinstance(x,str):
                    continue
                sValue += (x*pi[xCol])
                xCol += 1
            z = z/sValue
            zRow.append(z)
            cCol += 1
        cCol = 0
        rowSum = sum(zRow)

        zMatrix.append(zRow)
    return zMatrix

def mStep (zMatrix,pi):
    for j in range ((len(zMatrix[0])-1)):
        sum = 0
        tNR = 0
        for i in range ((len(zMatrix)-1)):
            sum += zMatrix[i][j]
            tNR += 1
        pi[j] = sum/tNR
    return pi

def outputCSV (information,pi):
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
            print(str(csv[i][j])+',',end='')
        print()

def printit():
    threading.Timer(300.0, printit).start()
    print ("Still working...")

if __name__ == '__main__':
    if verbose == True:
        print("GRAMMy2 0.1b\n")
        parseCommandLineArguments()

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
        pMatrix = initializePmatrix(pMatrix,totalNumberOfReads,len(pi)+1,information,BLASTFileArray)
        pMatrix = standardizeMatrixByColumn(pMatrix)

        print("4.Starting Abundance Calculation...")
        print("This could take a while perhaps you would like to grab a beverage...")

        printit()
        previousPi = pi
        zMatrix = eStep(pMatrix,pi)
        pi = mStep(zMatrix,pi)

        while pi != previousPi:
            previousPi = pi
            zMatrix = eStep(pMatrix,pi)
            pi = mStep(zMatrix,pi)

        print("5. Calculation Complete!")
        print("6. Printing results in CSV format!")
        outputCSV(information,pi)
        print("Exiting...")
    else:
        print("GRAMMy2 0.1b\n")
        parseCommandLineArguments()

        getBlastFileList(BLASTFileDir)

        information, totalNumberOfReads = processBLASTFiles(BLASTFileArray)

        information, pi = makePiVectorIndicies(information)
        pi, totalNumberOfReads = initializePiVector(BLASTFileArray,totalNumberOfReads)
        pi = standardizeVector(pi)

        initializeInformation(information)

        pMatrix = initializePmatrix(pMatrix,totalNumberOfReads,len(pi)+1,information,BLASTFileArray)
        pMatrix = standardizeMatrixByColumn(pMatrix)

        previousPi = pi
        zMatrix = eStep(pMatrix,pi)
        pi = mStep(zMatrix,pi)

        while pi != previousPi:
            previousPi = pi
            zMatrix = eStep(pMatrix,pi)
            pi = mStep(zMatrix,pi)

        outputCSV(information,pi)
        print("Exiting...")