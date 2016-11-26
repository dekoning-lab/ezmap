__author__ = 'patrickczeczko'

import os, subprocess
import Scripts.slurmScript as slurmScript


# Generates bash script to launch all required jobs within job manager
def generateSLURMScirpt(dataSets, projdir, configOptions, prinseqJobIDS):
    print('Setting up jobs for Step 2...')
    maxThreads = configOptions['slurm-max-num-threads']

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.environ["HISAT2_HOME"] = cwd + 'tools/HISAT2/'

    hisat2Path = configOptions['hisat2-path']

    # Checks to see if path ends in / character
    if not hisat2Path.endswith('/'):
        hisat2Path += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/HISAT2/' in hisat2Path:
        hisat2Path = hisat2Path.replace('cwd', cwd)

    if 'cwd/tools/HISAT2' in configOptions['hisat2-index-path']:
        hisat2IndexPath = configOptions['hisat2-index-path'].replace('cwd', cwd)
    else:
        hisat2IndexPath = configOptions['hisat2-index-path']

    script = open(projdir + '2-HumanMapping/hisat2Script.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'HISAT2', projdir + '2-HumanMapping/', configOptions)

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].hisat2OutputName + ' '
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
                       'COMMAND="' + hisat2Path + 'hisat2 ' +
                       '-p ${numCores} ' +
                       '-x ' + hisat2IndexPath + ' ' +
                       '-U ' + os.path.abspath(projdir) + '/1-Cleaning/${FILENAME}.fastq ' +
                       '-S ' + os.path.abspath(projdir) + '/2-HumanMapping/${FILENAMEOUTPUT}.sam"\n\n',
                       'srun $COMMAND'])
    script.close()


def generateSHScript(dataSets, projdir, configOptions):
    maxThreads = configOptions['slurm-max-num-threads']

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.environ["HISAT2_HOME"] = cwd + 'tools/HISAT2/'

    hisat2Path = configOptions['hisat2-path']

    # Checks to see if path ends in / character
    if not hisat2Path.endswith('/'):
        hisat2Path += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/HISAT2/' in hisat2Path:
        hisat2Path = hisat2Path.replace('cwd', cwd)

    if 'cwd/tools/HISAT2' in configOptions['hisat2-index-path']:
        hisat2IndexPath = configOptions['hisat2-index-path'].replace('cwd', cwd)
    else:
        hisat2IndexPath = configOptions['hisat2-index-path']

    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n# HISAT2 STEP\n'])

    script.write('echo "Staring Step 2 - HISAT2\\n\\n"\n\n')

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].prinseqOutputName + ' '
        fileOutputList += '' + dataSets[x].hisat2OutputName + ' '
        origFilePath = dataSets[x].projDirectory + '/'

    script.write('numCores=' + maxThreads + '\n\n')

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['COUNTER=0\n',
                       'while [  $COUNTER -lt ${#fileArray[@]} ];\n',
                       'do\n',
                       '\tTEMP=${fileArray[$COUNTER]}\n',
                       '\tTEMP2=${TEMP#\\\'}\n',
                       '\tFILENAME=${TEMP2%\\\'}\n\n',
                       '\tTEMP3=${fileOutputArray[$COUNTER]}\n',
                       '\tTEMP4=${TEMP3#\\\'}\n',
                       '\tFILENAMEOUTPUT=${TEMP4%\\\'}\n\n',
                       '\techo "Input file: ${FILENAME}"\n',
                       '\t' + hisat2Path + 'hisat2 ' +
                       '-p ${numCores} ' +
                       '-x ' + hisat2IndexPath + ' ' +
                       '-U ' + os.path.abspath(projdir) + '/1-Cleaning/${FILENAME}.fastq ' +
                       '-S ' + os.path.abspath(projdir) + '/2-HumanMapping/${FILENAMEOUTPUT}.sam\n\n',
                       '\tlet COUNTER=COUNTER+1\n',
                       'done\n'])

    script.close()


# Launch job to run within job manager
def processAllFiles(projDir, configOptions, dataSets):
    print('Starting step 2 jobs...')
    numOfFiles = len(dataSets)
    proc = subprocess.Popen(['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '2-HumanMapping/hisat2Script.sh'],
                            stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = []

    return jobIDS
