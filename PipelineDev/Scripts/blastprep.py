__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript

# Generates bash script to launch all required jobs within job manager
def generateSLURMScript(dataSets, projdir, configOptions, samtoolsJobIDS):
    print('Setting up jobs for Step 4...')

    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    script = open(projdir + '4-OrganismMapping/blastnScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 4, projdir + '4-OrganismMapping/', configOptions)

    IDList = ''
    for i in samtoolsJobIDS:
        IDList += ':' + str(i)

    script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write('## BLASTN PARAMETERS ##\n')

    print(configOptions)
    optionsString = ''
    for x in configOptions:
        if 'blastn-' in x:
            if not 'db-path' in x:
                param = x.replace('blastn-', '')
                value = configOptions[x]
                optionsString += param + ',' + str(value) + ','

    filelist = ''
    fileOutputList = ''
    for x in dataSets:
        filelist += '' + dataSets[x].samtoolsOutputName + ' '
        fileOutputList += '' + dataSets[x].blastnOutputName + ' '
        filePath = dataSets[x].projDirectory + '4-OrganismMapping/'

    script.write('fileArray=( ' + filelist + ')\n\n')
    script.write('fileOutputArray=( ' + fileOutputList + ')\n\n')

    script.write('optionString=' + optionsString[:-1] + '\n\n')

    script.writelines(['TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP2=${TEMP#\\\'}\n',
                       'FILENAME=${TEMP2%\\\'}\n\n',
                       '',
                       'TEMP3=${fileOutputArray[$SLURM_ARRAY_TASK_ID]}\n',
                       'TEMP4=${TEMP3#\\\'}\n',
                       'FILENAMEOUTPUT=${TEMP4%\\\'}\n\n'])

    script.write('echo "' +
                 configOptions['python3-path'] + ' ' +
                 cwd + 'Scripts/BLASTWithHitFilter.py ' +
                 cwd + 'tools/BLAST/ncbi-blast-2.2.30+/bin/blastn ' +
                 configOptions['blastn-db-path'] + ' '+
                 projdir + '3-UnmappedCollection/${FILENAME}.fasta'
                 ' ${optionString} ' +
                 configOptions['blastn-min-alignment-length'] +
                 ' ${FILENAMEOUTPUT}"')
