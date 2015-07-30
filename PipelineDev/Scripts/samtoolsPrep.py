__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript

# Generates bash script to launch all required jobs within job manager
def generateSLURMScript(dataSets, projdir, configOptions, bowtie2JobIDS):
    print('Setting up jobs for Step 3...')

    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    script = open(projdir + '3-UnmappedCollection/samtoolsScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 3, projdir + '3-UnmappedCollection/', configOptions)

    IDList = ''
    for i in bowtie2JobIDS:
        IDList += ':' + str(i)

    script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n')

    script.write('## SAMTOOLS PARAMETERS\n')
    script.writelines(['inFileDir=' + projdir + '2-HumanMapping/\n',
                       'outFileDir=' + projdir + '3-UnmappedCollection/\n',
                       'samtoolsPath=' + cwd + '/tools/SAMTOOLS/samtools\n\n'])

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].bowtie2OutputName + '.sam '
        fileOutputList += '' + dataSets[x].samtoolsOutputName + ' '
        filePath = dataSets[x].projDirectory + '3-UnmappedCollection/'

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
                       '${samtoolsPath} view -Sb - | '
                       '${samtoolsPath} view - | '
                       'awk \'{OFS="\\t"; print ">"$1"\\n"$10}\' - > ' + filePath + '${FILENAMEOUTPUT}.fasta',
                       '\n'])
    script.close()


# Launch job to run within job manager
def processAllFiles(projDir, configOptions, dataSets):
    print('Starting step 3 jobs...')
    numOfFiles = len(dataSets)

    proc = subprocess.Popen(
        ['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '3-UnmappedCollection/samtoolsScript.sh'],
        stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = [123456]

    return jobIDS
