__author__ = 'patrickczeczko'

import multiprocessing as mp
import os, sys

allInformation = {}
numOfDataChunks = 0
currentChunk = 0

outputFile = open('combinedGenomeData.csv', 'w+')
outputString = ""

# This function retrieves both the Genbank IDs as well as the genome lenghts
# from a .fna file containg all the genomes used in the previous BLAST step
def getNucleotideIDs(fileName):
    with open(fileName) as input_file:
        genomeLength = 0
        nucleotideID = -1
        for line in input_file:
            if line[0] == '>':
                if genomeLength != 0:
                    t = list(allInformation[nucleotideID])
                    t[2] = genomeLength
                    allInformation[nucleotideID] = tuple(t)
                    genomeLength = 0

                nucleotideID = line.split('|')[1]
                allInformation[nucleotideID] = (nucleotideID, 0, 0)
            else:
                genomeLength += len(line) - 1


# Process a section in the file to obtain a NCBI Taxonomy ID corresponding to the relative Genbank IDs
def processfile(fileName, start, stop, currentChunk, numOfDataChunks, outputQueue):
    outputArray = []

    print('Starting work on data partition ' + str(currentChunk) + ' of ' + str(numOfDataChunks))

    if start == 0 and stop == 0:
        with open(fileName) as input_file:
            for line in input_file:
                info = line.replace('\n', '').split('\t')

                nuclID = info[0]
                if nuclID in allInformation:
                    t = list(allInformation[nuclID])
                    t[1] = info[1]
                    allInformation[nuclID] = tuple(t)
                    outputString = str(t[0]) + ',' + str(t[1]) + ',' + str(t[2]) + ',\n'
                    outputArray.append(outputString)


    else:
        with open(fileName, 'r') as fh:
            fh.seek(start)
            lines = fh.readlines(stop - start)

            for line in lines:
                info = line.replace('\n', '').split('\t')

                nuclID = info[0]
                if nuclID in allInformation:
                    t = list(allInformation[nuclID])
                    t[1] = info[1]
                    allInformation[nuclID] = tuple(t)
                    outputString = str(t[0]) + ',' + str(t[1]) + ',' + str(t[2]) + '\n'
                    outputArray.append(outputString)

    outputQueue.put(outputArray)


# Reads in the file information and parses the taxonomy file in sections so that it can be processed in parallel
def readInTaxonInformation(fileName, cpu_count, currentChunk):
    # get file size and set chuck size
    filesize = os.path.getsize(fileName)
    split_size = 100 * 1024 * 1024

    # determine if it needs to be split
    if filesize > split_size:
        # create pool, initialize chunk start location (cursor)
        pool = mp.Pool(cpu_count)
        m = mp.Manager()
        outputQ = m.Queue()

        cursor = 0
        results = []
        with open(fileName, 'r') as fh:
            # for every chunk in the file...
            numOfDataChunks = (filesize // split_size)
            print(str(numOfDataChunks) + ' partitions of data to process')

            for chunk in range(filesize // split_size):

                # determine where the chunk ends, is it the last one?
                if cursor + split_size > filesize:
                    end = filesize
                else:
                    end = cursor + split_size

                # seek to end of chunk and read next line to ensure you
                # pass entire lines to the processfile function
                fh.seek(end)
                fh.readline()

                # get current file location
                end = fh.tell()

                # add chunk to process pool, save reference to get results
                proc = pool.apply_async(processfile,
                                        args=[fileName, cursor, end, currentChunk, numOfDataChunks, outputQ])
                currentChunk += 1
                results.append(proc)

                # setup next chunk
                cursor = end

        # close and wait for pool to finish
        pool.close()
        pool.join()

        while not outputQ.empty():
            array = outputQ.get()
            for x in array:
                outputFile.write(x)


if __name__ == '__main__':
    blastGenomeDBPath = sys.argv[1]
    gitaxiddmpPath = sys.argv[2]
    maxThreads = sys.argv[3]

    outputInfo = []

    print('Determining Genebank ID and Caluclating Genome Lengths.....')
    getNucleotideIDs(blastGenomeDBPath)

    print('Gather relavent taxon IDs.....')
    readInTaxonInformation(gitaxiddmpPath, maxThreads, currentChunk)

    print('Information has been written to file... exiting')