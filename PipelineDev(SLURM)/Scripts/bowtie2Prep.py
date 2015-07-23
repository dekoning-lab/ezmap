__author__ = 'patrickczeczko'

import os, subprocess
import Scripts.slurmScript as slurmScript

#SRR1024804
def generateSLURMScirpt(dataSets, projdir, configOptions, maxThreads, prinseqJobIDS):
    print('Setting up jobs for Step 2...')

    cwd = os.getcwd()
    # cwd = cwd.replace('(', '\(')
    # cwd = cwd.replace(')', '\)')

    os.environ["BOWTIE2_INDEXES"] = cwd + '/tools/BOWTIE2/'

    script = open(projdir + '2-HumanMapping/bowtie2Script.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 2, cwd, configOptions)

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].bowtie2OutputName + ' '
        origFilePath = dataSets[x].origFilePath + '/'

    IDList = ''
    for i in prinseqJobIDS:
        IDList += ':' + str(i)

    script.write('#SBATCH --dependency=afterok:' + IDList[1:] + '\n')

    script.write('numCores=' + maxThreads + '\n\n')

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n'
                       'echo "Input file: ${FILENAME}"\n',
                       'COMMAND="'+cwd + '/tools/BOWTIE2/bowtie2-2.2.5/bowtie2 --sensitive -x hg19 '
                             '-U ' + projdir + '1-Cleaning/${FILENAME}.fastq '
                                               '-S ' + projdir + '2-HumanMapping/${FILENAMEOUTPUT}.sam -p ${numCores}"\n\n',
                       'srun $COMMAND'])


def processAllFiles(projDir, numOfFiles, configOptions):
    print('Starting step 2 jobs...')
    proc = subprocess.Popen(['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '2-HumanMapping/bowtie2Script.sh'],
                            stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = [123456]

    return jobIDS
