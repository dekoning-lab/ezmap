__author__ = 'patrickczeczko'

import subprocess
import os


def generateSLURMScript(dataSets, projdir, configOptions):
    cwd = os.getcwd()
    script = open(projdir + '1-Cleaning/prinseqScript.sh', 'w+')

    script.writelines(['#!/bin/bash\n',
                       '#!/usr/bin/perl\n',
                       '#---------------------------------\n',
                       '# Mandatory settings\n',
                       '#SBATCH --job-name=VMAP-1\n',
                       '#SBATCH --workdir=' + cwd + '\n',
                       '#SBATCH --output=VMAP-1-%j' + '\n',
                       '#SBATCH --error=VMAP-1-%j' + '\n',
                       '#SBATCH --account=' + configOptions['slurm-account'] + '\n\n',
                       '# Resources required\n',
                       '#SBATCH --ntasks=1\n',
                       '#SBATCH --partition=' + configOptions['slurm-partition'] + '\n'])

    if configOptions['slurm-share'] == 'yes':
        script.write('#SBATCH --share\n')
    if configOptions['slurm-test-only'] == 'yes':
        script.write('#SBATCH --test-only\n')

    script.write('#---------------------------------\n\n')

    script.write('## PRINSEQ PARAMETERS\n')
    script.writelines(['out_format=3\n',
                       'min_qual_score=' + configOptions['prinseq-min_qual_score'] + '\n',
                       'lc_method=' + configOptions['prinseq-lc_method'] + '\n',
                       'lc_threshold=' + configOptions['prinseq-lc_threshold'] + '\n\n'])

    filelist = ''
    for x in dataSets:
        filelist += '\'' + dataSets[x].prinseqOutputName + '\' '

    script.write('fileArray = (' + filelist + ')\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       'perl -w ' + cwd + '/tools/' + 'prinseq-lite.pl '
                                                      '-fastq ${TEMP2} '
                                                      '-out_format $out_format '
                                                      '-min_qual_score $min_qual_score '
                                                      '-lc_method $lc_method '
                                                      '-lc_threshold $lc_threshold '
                                                      '-out_good '+projdir+'1-Cleaning/${FILENAME}'+
                                                      '-out_bad null '
                                                      '-log '
                                                      '\n'])


def processAllFiles(numOfFiles, projDir):
    output = subprocess.call(['sbatch', '--array=0' + str(numOfFiles), projDir + '1-Cleaning/prinseqScript.sh'])
    print(output)
