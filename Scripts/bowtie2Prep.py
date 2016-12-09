__author__ = 'patrickczeczko'

import os, subprocess
import Scripts.slurmScript as slurmScript

# Generates bash script to launch all required jobs within job manager
def generateSLURMScirpt(dataSets, projdir, configOptions, prinseqJobIDS):
    print('Setting up jobs for Step 2...')
    maxThreads = configOptions['slurm-max-num-threads']

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.environ["BOWTIE2_INDEXES"] = cwd + 'tools/BOWTIE2/'

    bowtie2Path = configOptions['bowtie2-path']

    # Checks to see if path ends in / character
    if not bowtie2Path.endswith('/'):
        bowtie2Path += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BOWTIE2/' in bowtie2Path:
        bowtie2Path = bowtie2Path.replace('cwd', cwd)

    script = open(projdir + '2-HumanMapping/bowtie2Script.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'BOWTIE2', projdir + '2-HumanMapping/', configOptions)

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].bowtie2OutputName + ' '
        origFilePath = dataSets[x].projDirectory + '/'

    IDList = ''
    for i in prinseqJobIDS:
        IDList += ':' + str(i)

    if prinseqJobIDS:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n')

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
                       'COMMAND="' + bowtie2Path + 'bowtie2 --sensitive ' +
                       '-x ' + cwd + '/tools/BOWTIE2/hg19/hg19 ' +
                       '-U ' + os.path.abspath(projdir) + '/1-Cleaning/${FILENAME}.fastq ' +
                       '-S ' + os.path.abspath(projdir) + '/2-HumanMapping/${FILENAMEOUTPUT}.sam -p ${numCores}"\n\n',
                       'srun $COMMAND'])
    script.close()

    os.chmod(projdir + '2-HumanMapping/bowtie2Script.sh', 0o755)

def generateSHScript(dataSets, projdir, configOptions):
    maxThreads = configOptions['slurm-max-num-threads']

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.environ["BOWTIE2_INDEXES"] = cwd + 'tools/BOWTIE2/'

    bowtie2Path = configOptions['bowtie2-path']

    # Checks to see if path ends in / character
    if not bowtie2Path.endswith('/'):
        bowtie2Path += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BOWTIE2/' in bowtie2Path:
        bowtie2Path = bowtie2Path.replace('cwd', cwd)

    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n# BOWTIE2 STEP\n'])

    script.write('echo "Staring Step 2 - BOWTIE2\\n\\n"\n\n')

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].bowtie2OutputName + ' '
        origFilePath = dataSets[x].projDirectory + '/'

    script.write('numCores=' + maxThreads + '\n\n')

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['COUNTER=0\n',
                       'while [  $COUNTER -lt ${#fileArray[@]} ];\n',
                       'do\n',
                       'TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n'
                       'echo "Input file: ${FILENAME}"\n',
                       '\t' + bowtie2Path + 'bowtie2 --sensitive ' +
                       '-x ' + cwd + '/tools/BOWTIE2/hg19/hg19 ' +
                       '-U ' + os.path.abspath(projdir) + '/1-Cleaning/${FILENAME}.fastq ' +
                       '-S ' + os.path.abspath(projdir) + '/2-HumanMapping/${FILENAMEOUTPUT}.sam -p ${numCores}"\n\n',
                       '\tlet COUNTER=COUNTER+1\n',
                       'done\n'])
    script.close()

# Launch job to run within job manager
def processAllFiles(projDir, configOptions, dataSets):
    print('Starting step 2 jobs...')
    numOfFiles = len(dataSets)
    proc = subprocess.Popen(['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '2-HumanMapping/bowtie2Script.sh'],
                            stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = []

    return jobIDS
