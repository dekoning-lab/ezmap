import subprocess, math, os, sys

def splitFASTQ (file, numChunks):
    print("Splitting "+file+" into "+str(numChunks)+" new files")

    result = subprocess.getoutput("wc -l "+file)

    numLines = int(result.split()[0])
    numReads = numLines/4

    numReadsPerChunk = math.floor(numReads/numChunks)

    filenameHead = os.path.splitext(os.path.basename(file))[0]
    filePath = os.path.dirname(os.path.abspath(file))

    result = subprocess.getoutput("split -l "+str(int(numReadsPerChunk*4))+" "+file+" "+filePath+"/"+filenameHead+"-")

    for i in range(1,numChunks+1):
        subprocess.getoutput("mv "+filePath+"/"+filenameHead+"-"+chr(int(math.floor(i/26))+97)+""+chr(i+96)+" "+filePath+"/"+filenameHead+".part"+str(i)+".fastq")

file = sys.argv[1]
chunks = int(sys.argv[2])

splitFASTQ(file,chunks)
