import os

fastqDir = "/hyperion/work/patrick/quake-data/prinseqResults-minQual21/"
samDir ="/hyperion/work/patrick/quakeDataMapping/"

missedFiles = []

for file in os.listdir(fastqDir):
    if '.log' not in file:
        if not os.path.exists(samDir+file+'.sam'):
            missedFiles.append(file)

for fileName in os.listdir(samDir):
	if '.errs' in fileName:
		file = open(fileName)
		fileLine = file.readline()

		if 'Error' in fileLine:
			outFileName = fileName.replace(".errs",".out")
			outFile = open(outFileName)
			readline = outFile.readline()
			readline =outFile.readline()
			
			readline = readline.replace ("Input file: ","")
			readline = readline.replace ("\n","")
			missedFiles.append(readline)

missedFiles = ['SRR1024998_prinseq_good_EQh2.fastq']

print missedFiles


