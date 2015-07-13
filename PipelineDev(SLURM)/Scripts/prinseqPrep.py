__author__ = 'patrickczeczko'
import itertools


def generateSLURMScript(dataSets, projdir):
    script = open(projdir + '1-Cleaning/prinseqScript.sh', 'w+')

    script.writelines(['#!/bin/bash\n',
                       '#!/usr/bin/perl\n',
                       '#---------------------------------\n\n',
                       '# Mandatory settings\n',
                       '#SBATCH --job-name=\n',
                       '#SBATCH --workdir=\n',
                       '#SBATCH --output=\n',
                       '#SBATCH --errors=\n',
                       '#SBATCH --account=\n\n',
                       '# Resources required\n',
                       '#SBATCH --ntasks=\n',
                       '#SBATCH --partition=\n',
                       '#---------------------------------\n\n'
                       ])

    script.write('## PRINSEQ PARAMETERS\n')
    script.writelines(['out_format=\n',
                       'min_qual_score=\n',
                       'lc_method=\n',
                       'lc_threshold=\n\n'])

    filelist = ''
    for x in dataSets:
        filelist += '\'' + dataSets[x].prinseqOutputName + '\' '

    script.write('fileArray = (' + filelist + ')\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       'perl -w prinseq-lite.pl -fastq ${TEMP2} -out_format $out_format -log  -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold -out_bad null\n'])
