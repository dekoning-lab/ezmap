__author__ = 'patrickczeczko'

import subprocess
import os
import Scripts.slurmScript as slurmScript


# Generates bash script to launch all required jobs within job manager
def generatePreScript(dataSets, projdir, configOptions, blastjobids):
    print('Setting up jobs for Step 5...')

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    projdir = os.path.abspath(projdir) + '/'

    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + '5-RelativeAbundanceEstimation/emalPreScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'EMALPREP', projdir + '5-RelativeAbundanceEstimation/', configOptions)

    IDList = ''
    for i in blastjobids:
        IDList += ':' + str(i)

    if blastjobids:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write(
        'srun ' +
        configOptions['python3-path'] + ' ' + emalPath + 'EMAL-DataPrep.py ' +
        configOptions['blast-db-path'] + ' ' +
        configOptions['emal-gi-taxid-nucldmp-path'] + ' ' +
        '1' + ' ' +
        projdir + '5-RelativeAbundanceEstimation/' +
        ' ' + configOptions['project-name'])

    script.close()
    os.chmod(projdir + '5-RelativeAbundanceEstimation/emalPreScript.sh', 0o755)

    return 'emalPreScript.sh'


def generateSHPreScript(dataSets, projdir, configOptions):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    projdir = os.path.abspath(projdir) + '/'

    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n# EMAL PREP STEP\n'])
    script.write('echo "Staring Step 5 - EMAL PREP\\n\\n"\n\n')

    script.writelines([configOptions['python3-path'] + ' ' + emalPath + 'EMAL-DataPrep.py ' +
                       configOptions['blast-db-path'] + ' ' +
                       configOptions['emal-gi-taxid-nucldmp-path'] + ' ' +
                       configOptions['slurm-max-num-threads'] + ' ' +
                       projdir + '5-RelativeAbundanceEstimation/' +
                       ' ' + configOptions['project-name']])
    script.close()


def generateMainScript(dataSets, projdir, configOptions, emalPrejobids):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projdir = os.path.abspath(projdir) + '/'
    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + '5-RelativeAbundanceEstimation/emalScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'EMAL', projdir + '5-RelativeAbundanceEstimation/', configOptions)

    IDList = ''
    for i in emalPrejobids:
        IDList += ':' + str(i)

    if emalPrejobids:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write(
        'srun ' +
        configOptions['python3-path'] + ' ' + emalPath + 'EMAL-Main.py ' +
        '-d ' + projdir + '4-OrganismMapping/ ' +
        '-v -t ' + configOptions['slurm-max-num-threads'] + ' ' +
        '-c ' + configOptions['project-name'] + '.gra ' +
        '-m ' + configOptions['emal-acceptance-value'] + ' ' +
        '-o ' + projdir + '5-RelativeAbundanceEstimation/ ' +
        '-e .tsv '
        '-i ' + configOptions['project-name'] + '-combinedGenomeData.csv')

    script.close()
    os.chmod(projdir + '5-RelativeAbundanceEstimation/emalScript.sh', 0o755)

    return 'emalScript.sh'


def generateSHMainScript(dataSets, projdir, configOptions):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projdir = os.path.abspath(projdir) + '/'
    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n\n# EMAL MAIN STEP\n'])
    script.write('echo "Staring Step 6 - EMAL MAIN\\n\\n"\n\n')

    script.writelines([configOptions['python3-path'] + ' ' + emalPath + 'EMAL-Main.py ' +
                       '-d ' + projdir + '4-OrganismMapping/ ' +
                       '-v -t ' + configOptions['slurm-max-num-threads'] + ' ' +
                       '-c ' + configOptions['project-name'] + '.gra ' +
                       '-m ' + configOptions['emal-acceptance-value'] + ' ' +
                       '-o ' + projdir + '5-RelativeAbundanceEstimation/ ' +
                       '-e .tsv '
                       '-i ' + projdir + '5-RelativeAbundanceEstimation/' + configOptions['project-name'] + '-combinedGenomeData.csv'])
    script.close()


def generatePostScript(dataSets, projdir, configOptions, emalJobIDS):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projdir = os.path.abspath(projdir) + '/'
    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + '5-RelativeAbundanceEstimation/emalPostScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'EMALPOST', projdir + '5-RelativeAbundanceEstimation/', configOptions)

    IDList = ''
    for i in emalJobIDS:
        IDList += ':' + str(i)

    if emalJobIDS:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write(
        'srun ' +
        configOptions['python3-path'] + ' ' + emalPath + 'EMAL-Post.py ' +
        '-f ' + projdir + '5-RelativeAbundanceEstimation/' + configOptions['project-name'] + '.gra ' +
        '-c ' + configOptions['project-name'] + '-emal.csv ' +
        '-o ' + projdir + '5-RelativeAbundanceEstimation/')

    script.close()
    os.chmod(projdir + '5-RelativeAbundanceEstimation/emalPostScript.sh', 0o755)

    return 'emalPostScript.sh'


def generateSHPostScript(dataSets, projdir, configOptions):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projdir = os.path.abspath(projdir) + '/'
    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    script = open(projdir + 'ezmapScript.sh', 'a+')

    script.writelines(['\n\n# EMAL POST STEP\n'])
    script.write('echo "Staring Step 7 - EMAL POST\\n\\n"\n\n')

    script.writelines([configOptions['python3-path'] + ' ' + emalPath + 'EMAL-Post.py ' +
                       '-f ' + projdir + '5-RelativeAbundanceEstimation/' + configOptions['project-name'] + '.gra ' +
                       '-c ' + configOptions['project-name'] + '-emal.csv ' +
                       '-o ' + projdir + '5-RelativeAbundanceEstimation/'])
    script.close()

# Launch job to run within job manager
def processAllFiles(projDir, configOptions, dataSets, stepNum, scriptName):
    print('Queueing step 5-' + str(stepNum) + '...')
    numOfFiles = len(dataSets)
    proc = subprocess.Popen(
        ['sbatch', projDir + '5-RelativeAbundanceEstimation/' + scriptName],
        stdout=subprocess.PIPE)

    outs, errs = proc.communicate()
    outs = str(outs).strip('b\'Submitted batch job ').strip('\\n')

    jobIDS = []
    jobIDS.append(int(outs))

    if configOptions['slurm-test-only'] == 'yes':
        jobIDS = []

    return jobIDS
