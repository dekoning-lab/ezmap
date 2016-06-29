import os, sys

inputSeqNum = 0   # Input sequences:
inputBasesNum = 0 # Input bases:
inputMeanLen = 0  # Input mean length:
numGoodSeq = 0    # Good sequences:
numGoodBases = 0  # Good bases:
goodMeanLen = 0   # Good mean length:
numBadSeq = 0     # Bad sequences:
numBadBase = 0    # Bad bases:
badMeanLen = 0    # Bad mean length:
totalFiles = 0

for item in sys.argv:
    if 'part' in item:

        file = open(item,'r')
        for line in file:
            if "Input sequences: " in line:
                # print(int(line.split("Input sequences: ")[1].rstrip("\n").replace(',','')))
                inputSeqNum += int(line.split("Input sequences: ")[1].rstrip("\n").replace(',',''))

            elif "Input bases: " in line:
                # print(int(line.split("Input bases: ")[1].rstrip("\n").replace(',', '')))
                inputBasesNum += int(line.split("Input bases: ")[1].rstrip("\n").replace(',', ''))

            elif "Input mean length: " in line:
                # print(float(line.split("Input mean length: ")[1].rstrip("\n").replace(',', '')))
                inputMeanLen += float(line.split("Input mean length: ")[1].rstrip("\n").replace(',', ''))

            elif "Good sequences: " in line:
                # print(int(line.split("Good sequences: ")[1].split(" (")[0].rstrip("\n").replace(',', '')))
                numGoodSeq += int(line.split("Good sequences: ")[1].split(" (")[0].rstrip("\n").replace(',', ''))

            elif "Good bases:" in line:
                # print(int(line.split("Good bases: ")[1].rstrip("\n").replace(',', '')))
                numGoodBases += int(line.split("Good bases: ")[1].rstrip("\n").replace(',', ''))

            elif "Good mean length:" in line:
                # print(float(line.split("Good mean length: ")[1].rstrip("\n").replace(',', '')))
                goodMeanLen += float(line.split("Good mean length: ")[1].rstrip("\n").replace(',', ''))
                # print(goodMeanLen)

            elif "Bad sequences:" in line:
                # print(int(line.split("Bad sequences: ")[1].split(" (")[0].rstrip("\n").replace(',', '')))
                numBadSeq += int(line.split("Bad sequences: ")[1].split(" (")[0].rstrip("\n").replace(',', ''))

            elif "Bad bases:" in line:
                # print(int(line.split("Bad bases: ")[1].rstrip("\n").replace(',', '')))
                numBadBase += int(line.split("Bad bases: ")[1].rstrip("\n").replace(',', ''))

            elif "Bad mean length:" in line:
                # print(float(line.split("Bad mean length: ")[1].rstrip("\n").replace(',', '')))
                badMeanLen += float(line.split("Bad mean length: ")[1].rstrip("\n").replace(',', ''))

        totalFiles += 1

inputMeanLen = inputMeanLen/float(totalFiles)
goodMeanLen = goodMeanLen/float(totalFiles)
badMeanLen = badMeanLen/float(totalFiles)

outFile = open(sys.argv[1], 'w+')

outFile.write('Input sequences: '+str(inputSeqNum)+'\n')
outFile.write('Input bases: '+str(inputBasesNum)+'\n')
outFile.write('Input mean length: '+str(inputMeanLen)+'\n')
outFile.write('Good sequences: '+str(numGoodSeq)+'\n')
outFile.write('Good bases: '+str(numGoodBases)+'\n')
outFile.write('Good mean length: '+str(goodMeanLen)+'\n')
outFile.write('Bad sequences: '+str(numBadSeq)+'\n')
outFile.write('Bad bases: '+str(numBadBase)+'\n')
outFile.write('Bad mean length: '+str(badMeanLen)+'\n')
