import os, sys
import re

def readInfoFromLogFile (dir,file):
	print("Reading information from "+file)
	absolutePath = dir+"/"+file

	logFile = open(absolutePath)

	results =[0,0,0,0]

	for line in logFile:
		if 'Input sequences: ' in line:
			num = re.split('Input sequences: ',line)[1]
			num = num.replace(",","")
			results[0] = num
		elif 'Good sequences: ' in line:
			num = re.split('Good sequences: ',line)[1]
			num = re.split('\(',num)[0]
			num = num.replace(",","")
			results[1] = num
		elif 'Bad sequences: ' in line:
			num = re.split('Bad sequences: ',line)[1]
			num = re.split('\(',num)[0]
			num = num.replace(",","")
			results[2] = num
		elif 'min_qual_score: ' in line:
			num = re.split('min_qual_score: ',line)[1]
			num = num.replace(",","")
			results[3] = num
	
	return results

def printResults (totalSeq,totalGoodSeq,totalBadSeq,totalRmLowQual):
	print("\n\nResults:")
	print(("Total Sequences: ").ljust(30," ")+str(totalSeq).ljust(20," "))
	print(("Total Good Sequences: ").ljust(30," ")+str(totalGoodSeq).ljust(20," "))#+str((totalGoodSeq/totalSeq)*100)+'%')
	print(("Total Bad Sequences: ").ljust(30," ")+str(totalBadSeq).ljust(20," "))#+str((totalGoodSeq/totalSeq)*100)+'%')
	print(("Total Low Quality Sequences: ").ljust(30," ")+str(totalRmLowQual).ljust(20," "))#+str((totalGoodSeq/totalSeq)*100)+'%')

if __name__ == "__main__":
	totalSeq = 0
	totalGoodSeq = 0
	totalBadSeq = 0
	totalRmLowQual = 0

	numOfFiles = 0

	dir = sys.argv[1]

	print ("\nScanning for Log Files....\n")

	for file in os.listdir(dir):
		if file.endswith('.fastq.log'):
			results = readInfoFromLogFile(dir,file)

			totalSeq += int(results[0])
			totalGoodSeq += int(results[1])
			totalBadSeq += int(results[2])
			totalRmLowQual += int(results[3])

			numOfFiles += 1
	print (str(numOfFiles)+" Log file(s) found.....")
	print (totalSeq,totalGoodSeq,totalBadSeq,totalRmLowQual)
	printResults(totalSeq,totalGoodSeq,totalBadSeq,totalRmLowQual)



