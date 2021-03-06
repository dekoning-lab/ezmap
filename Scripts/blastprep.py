__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript


# Generates bash script to launch all required jobs within job manager
def generateSLURMScript(dataSets, projdir, configOptions, samtoolsJobIDS):
    print('Setting up jobs for Step 4...')

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    projdir = os.path.abspath(projdir) + '/'

    blastPath = configOptions['blast-path']

    # Checks to see if path ends in / character
    if not blastPath.endswith('/'):
        blastPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BLAST/' in blastPath:
        blastPath = blastPath.replace('cwd', cwd)

    script = open(projdir + '4-OrganismMapping/blastnScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'BLAST', projdir + '4-OrganismMapping/', configOptions)

    IDList = ''
    for i in samtoolsJobIDS:
        IDList += ':' + str(i)

    # Add job dependencies so new jobs wont start until previous ones have been completed
    if samtoolsJobIDS:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write('## BLASTN PARAMETERS ##\n')

    optionsString = ''
    for x in configOptions:
        if 'blast-' in x:
            if 'db-path' and '-path' not in x:
                if not 'min-alignment-length' in x:
                    param = x.replace('blast-', '')
                    value = configOptions[x]
                    optionsString += param + ',' + str(value) + ','

    optionsString += 'outfmt,' + '6,'
    optionsString += 'num_threads,' + configOptions['slurm-max-num-threads'] + ','

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].samtoolsOutputName + ' '
        fileOutputList += '' + dataSets[x].blastnOutputName + ' '
        filePath = dataSets[x].projDirectory + '4-OrganismMapping/'

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.write('optionString=' + optionsString[:-1] + '\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n'])

    script.write('srun ' +
                 configOptions['python3-path'] + ' ' +
                 cwd + '/tools/BLAST/BLASTWithHitFilter.py ' +
                 blastPath + 'blastn ' +
                 configOptions['blast-db-path'] + ' ' +
                 projdir + '3-UnmappedCollection/${FILENAME}.fasta' +
                 ' ${optionString} ' +
                 projdir + '4-OrganismMapping/ ' +
                 configOptions['blast-min-alignment-length'] +
                 ' ${FILENAMEOUTPUT}')
    script.close()

    os.chmod(projdir + '4-OrganismMapping/blastnScript.sh', 0o755)


def generateSHScript(dataSets, projdir, configOptions):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    projdir = os.path.abspath(projdir) + '/'

    blastPath = configOptions['blast-path']

    # Checks to see if path ends in / character
    if not blastPath.endswith('/'):
        blastPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BLAST/' in blastPath:
        blastPath = blastPath.replace('cwd', cwd)
    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n# BLAST STEP\n'])
    script.write('echo "Staring Step 4 - BLAST\\n\\n"\n\n')

    script.write('# BLASTN PARAMETERS ##\n')

    optionsString = ''
    for x in configOptions:
        if 'blast-' in x:
            if 'db-path' and '-path' not in x:
                if not 'min-alignment-length' in x:
                    param = x.replace('blast-', '')
                    value = configOptions[x]
                    optionsString += param + ',' + str(value) + ','

    optionsString += 'outfmt,' + '6,'
    optionsString += 'num_threads,' + configOptions['slurm-max-num-threads'] + ','

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].samtoolsOutputName + ' '
        fileOutputList += '' + dataSets[x].blastnOutputName + ' '
        filePath = dataSets[x].projDirectory + '4-OrganismMapping/'

    script.write('fileArray=( ' + filelist + ')\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.write('optionString=' + optionsString[:-1] + '\n\n')

    script.writelines(['COUNTER=0\n',
                       'while [  $COUNTER -lt ${#fileArray[@]} ];\n',
                       'do\n',
                       '\tTEMP=${fileArray[$COUNTER]}\n',
                       '\tTEMP2=${TEMP#\\\'}\n',
                       '\tFILENAME=${TEMP2%\\\'}\n\n',
                       '\tTEMP3=${fileOutputArray[$COUNTER]}\n',
                       '\tTEMP4=${TEMP3#\\\'}\n',
                       '\tFILENAMEOUTPUT=${TEMP4%\\\'}\n\n',
                       '\t' + configOptions['python3-path'] + ' ' +
                       cwd + '/tools/BLAST/BLASTWithHitFilter.py ' +
                       blastPath + 'blastn ' +
                       configOptions['blast-db-path'] + ' ' +
                       projdir + '3-UnmappedCollection/${FILENAME}.fasta' +
                       ' ${optionString} ' +
                       projdir + '4-OrganismMapping/ ' +
                       configOptions['blast-min-alignment-length'] +
                       ' ${FILENAMEOUTPUT}\n',
                       '\tlet COUNTER=COUNTER+1\n',
                       'done\n'])
    script.close()


# Launch job to run within job manager
def processAllFiles(projDir, configOptions, dataSets):
    print('Queueing step 4...')
    numOfFiles = len(dataSets)
    proc = subprocess.Popen(
        ['sbatch', '--array=0-' + str(numOfFiles - 1), projDir + '4-OrganismMapping/blastnScript.sh'],
        stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    for x in range(numOfFiles):
        jobIDS.append(int(outs) + x)
    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = []

    return jobIDS
