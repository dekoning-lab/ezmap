__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript


def generateSLURMScript(dataSets, projdir, configOptions, bowtie2JobIDS):
    print('Setting up jobs for Step 3...')

    cwd = os.getcwd()
    cwd = cwd.replace('(', '\(')
    cwd = cwd.replace(')', '\)')

    script = open(projdir + '3-UnmappedCollection/samtoolsScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 3, cwd, configOptions)

    IDList = ''
    for i in bowtie2JobIDS:
        IDList += ':' + str(i)

    script.write('#SBATCH --dependency=afterok:' + IDList[1:] + '\n')

    script.write('## SAMTOOLS PARAMETERS\n')
    script.writelines(['inFileDir=' + projdir + '/2-HumanMapping/\n',
                       'outFileDir=' + projdir + '/3-UnmappedCollection/\n',
                       'samtoolsPath=/hyperion/work/patrick/quakeDataMapping/samtools-1.2/samtools\n\n'])

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].bowtie2OutputName + '.sam '
        fileOutputList += '' + dataSets[x].samtoolsOutputName + ' '
        filePath = dataSets[x].projDirectory + '/2-HumanMapping/'

    script.write('fileArray=( ' + filelist + ')\n\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n',
                       '',
                       'echo ${FILENAME} $SLURM_ARRAY_TASK_ID $TEMP \n\n',
                       'srun '
                       '${samtoolsPath} view -f4 ${inFileDir}${FILENAME} | '
                       '${samtoolsPath} view -Sb | '
                       '${samtoolsPath} view | '
                       'awk \'{OFS="\t"; print ">"$1"\n"$10}\' - > ' + filePath + '${FILENAMEOUTPUT}.fasta',
                       '\n'])
    script.close()
