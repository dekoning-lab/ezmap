__author__ = 'patrickczeczko'

import os
import Scripts.slurmScript as slurmScript


def generateSLURMScirpt(dataSets, projdir, configOptions, maxThreads):
    print('Setting up jobs for Step 2...')

    cwd = os.getcwd()
    cwd = cwd.replace('(', '\(')
    cwd = cwd.replace(')', '\)')

    os.environ["BOWTIE2_INDEXES"] = cwd+'/tools/BOWTIE2/'

    print(os.environ["BOWTIE2_INDEXES"])

    script = open(projdir + '2-HumanMapping/bowtie2Script.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 2, cwd, configOptions)

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].bowtie2OutputName + ' '
        origFilePath = dataSets[x].origFilePath + '/'

    script.write('numCores=' + maxThreads + '\n\n')

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['TEMP=${fileArray[${SLURM_ARRAY_TASK_ID}]}\n',
                       'TEMP2=${TEMP#\'}\n',
                       'FILENAME=${TEMP2%\'}\n\n',
                       'TEMP3=${fileOutputArray[${SLURM_ARRAY_TASK_ID}]}\n',
                       'TEMP4=${TEMP3#\'}\n',
                       'FILEOUTPUTNAME=${TEMP4%\'}\n\n',
                       'echo "Input file: ${TEMP2}"\n',
                       cwd + '/tools/BOWTIE2/bowtie2-2.2.5/bowtie2 --sensitive -x hg19 '
                             '-U ' + projdir + '1-Cleaning/${FILENAME} '
                                               '-S ' + projdir + '2-HumanMapping/${FILEOUTPUTNAME}.sam -p ${numCores}\n\n',
                       ''])
