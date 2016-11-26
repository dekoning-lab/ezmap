__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript


# Generates bash script to launch all required jobs within job manager
def generateSLURMScript(dataSets, projdir, configOptions):
    print('Setting up jobs for Step 1...')

    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    prinseqPath = configOptions['prinseq-path']

    # Checks to see if path ends in / character
    if not prinseqPath.endswith('/'):
        prinseqPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/PRINSEQ/' in prinseqPath:
        prinseqPath = prinseqPath.replace('cwd/', cwd)

    script = open(projdir + '1-Cleaning/prinseqScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'PRINSEQ', projdir + '1-Cleaning/', configOptions)

    script.write('## PRINSEQ PARAMETERS\n')
    script.writelines(['out_format=3\n',
                       'min_qual_score=' + configOptions['prinseq-min_qual_score'] + '\n',
                       'lc_method=' + configOptions['prinseq-lc_method'] + '\n',
                       'lc_threshold=' + configOptions['prinseq-lc_threshold'] + '\n\n'])

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].origFileName + ' '
        fileOutputList += '' + dataSets[x].prinseqOutputName + ' '
        origFilePath = dataSets[x].origFilePath + '/'

    script.write('fileArray=( ' + filelist + ')\n\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n'
                       'echo ${FILENAME} $SLURM_ARRAY_TASK_ID $TEMP \n' +
                       '' + prinseqPath + 'prinseqMultipleThread.sh ' + os.path.abspath(origFilePath) + '/ ${TEMP} ' +
                       os.path.abspath(projdir) + '/1-Cleaning/ ' + prinseqPath + ' ' +
                       configOptions['slurm-max-num-threads'] + ' 3 ' + configOptions['prinseq-min_qual_score'] + ' ' +
                       configOptions['prinseq-lc_method'] + ' ' + configOptions['prinseq-lc_threshold'] + ' ' +
                       configOptions['python3-path'] + ' \n'])
    script.close()

    os.chmod(projdir + '1-Cleaning/prinseqScript.sh', 0o755)
    os.chmod(prinseqPath + 'combineLogFiles.py', 0o755)
    os.chmod(prinseqPath + 'fastq-splitter.pl', 0o755)
    os.chmod(prinseqPath + 'prinseq-lite.pl', 0o755)
    os.chmod(prinseqPath + 'prinseqMultipleThread.sh', 0o755)

def generateSHScript (dataSets, projdir, configOptions):
    # Get the current working directory and path to PRINSEQ
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')
    prinseqPath = configOptions['prinseq-path']

    # Checks to see if path ends in / character
    if not prinseqPath.endswith('/'):
        prinseqPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/PRINSEQ/' in prinseqPath:
        prinseqPath = prinseqPath.replace('cwd/', cwd)

    script = open(projdir + 'ezmapScript.sh', 'w+')

    script.write('## PRINSEQ PARAMETERS\n')
    script.writelines(['out_format=3\n',
                       'min_qual_score=' + configOptions['prinseq-min_qual_score'] + '\n',
                       'lc_method=' + configOptions['prinseq-lc_method'] + '\n',
                       'lc_threshold=' + configOptions['prinseq-lc_threshold'] + '\n\n'])

    script.writelines(['PRINSEQ STEP\n'])

    for x in dataSets:
        print (x)

        script.write('')


    script.close()

    os.chmod(projdir + 'ezmapScript.sh', 0o755)
    os.chmod(prinseqPath + 'combineLogFiles.py', 0o755)
    os.chmod(prinseqPath + 'fastq-splitter.pl', 0o755)
    os.chmod(prinseqPath + 'prinseq-lite.pl', 0o755)
    os.chmod(prinseqPath + 'prinseqMultipleThread.sh', 0o755)

def processAllFiles(projDir, configOptions, dataSets):
    print('Starting step 1 jobs...')
    numOfFiles = len(dataSets)

    proc = subprocess.Popen(['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '1-Cleaning/prinseqScript.sh'],
                            stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = [123456]

    return jobIDS
