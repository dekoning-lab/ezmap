import os


dir = "/hyperion/work/patrick/quake-data/originalData/"

countMissingFiles = 0
countTotalFiles = 0
fileName = ''

arrayOfMissingFiles = []

for file in os.listdir(dir):
	if file.endswith(".fastq"):
		fileName = os.path.splitext(file)[0]
		if len(fileName) == 10:
			countTotalFiles += 1
			if (not os.path.isfile(fileName+'.fastq.log')):
				countMissingFiles += 1
				#print ('Missing log file for '+fileName+'.fastq ('+str(os.path.getsize(fileName+'.fastq')/(1024*1024*1024))+' GB)')
				arrayOfMissingFiles.append(fileName+'.fastq')

arrayOfMissingFiles = ['SRR1024599.fastq','SRR1024689.fastq']

print arrayOfMissingFiles