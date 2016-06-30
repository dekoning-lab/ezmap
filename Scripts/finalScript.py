__author__ = 'patrickczeczko'
import subprocess, os
import Scripts.slurmScript as slurmScript


def collectPipelineResult(projName, projDir, configOptions, finalJobIDS):
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    script = open(projDir + '6-FinalResult-' + projName + '/information/resultsScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 'FINALRESULTS', projDir + '6-FinalResult/', configOptions)

    IDList = ''
    for i in finalJobIDS:
        IDList += ':' + str(i)

    if finalJobIDS:
        script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write(
        configOptions['python3-path'] + ' ' + cwd + 'Scripts/gatherResults.py ' + projDir + ' ' + projName)

    command = 'sbatch -p ' + configOptions['slurm-partition'] + ' -J EZMAP-FINALRESULTS --wrap "sh ' + os.path.abspath(
        projDir) + '/6-FinalResult-' + projName + '/information/resultsScript.sh' + '"'

    os.system(command)
