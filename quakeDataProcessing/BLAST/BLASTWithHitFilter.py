__author__ = 'patrickczeczko'

import os, sys
import subprocess
import shlex


def execute(command, filename):
    print('/hyperion/work/patrick/quakeData/BLASTResults/BLASTMIN45LEN/' + filename + '.tsv')
    outputFile = open('/hyperion/work/patrick/quakeData/BLASTResults/BLASTMIN45LEN/' + filename + '.tsv', 'w+')
    popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        line = line.decode()
        if int(line.split('\t')[3]) >= 45:
            outputFile.write(line)


if __name__ == "__main__":
    fileName = sys.argv[1]
    print(sys.argv)
    command = '/hyperion/work/patrick/quakeDataProcessing/BLAST/ncbi-blast-2.2.30+/bin/blastn -db /hyperion/work/patrick/quakeDataProcessing/BLAST/ncbi-blast-2.2.30+/db/viral.1.1.genomic.fna -query /hyperion/work/patrick/quakeData/BLASTResults/fasta/MPT3.0/' + fileName + ' -task blastn -dust no -reward 1 -penalty -3 -word_size 12 -gapopen 5 -gapextend 2 -evalue 0.0001 -perc_identity 90 -outfmt 6 -num_threads 8'
    commmand = shlex.split(command)
    execute(command, os.path.splitext(fileName)[0])
