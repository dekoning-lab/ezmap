__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript


def generateSLURMScript(dataSets, projdir, configOptions):
    print('Setting up jobs for Step 1...')

    cwd = os.getcwd()
    cwd = cwd.replace('(', '\(')
    cwd = cwd.replace(')', '\)')

    script = open(projdir + '1-Cleaning/prinseqScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 1, cwd, configOptions)

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
                       'echo ${FILENAME} $SLURM_ARRAY_TASK_ID $TEMP \n'
                       'perl -w ' + cwd + '/tools/PRINSEQ/' + 'prinseq-lite.pl '
                                                              '-fastq ' + origFilePath + '${TEMP2} '
                                                                                         '-out_format $out_format '
                                                                                         '-min_qual_score $min_qual_score '
                                                                                         '-lc_method $lc_method '
                                                                                         '-lc_threshold $lc_threshold '
                                                                                         '-out_good ' + projdir + '1-Cleaning/${FILENAMEOUTPUT} ' +
                       '-out_bad null '
                       '-log '
                       '\n'])


def processAllFiles(numOfFiles, projDir, configOptions):
    print('Starting step 1 jobs...')
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

