__author__ = 'patrickczeczko'
import subprocess, os
import Scripts.slurmScript as slurmScript


def collectPipelineResult(projName, projDir, configOptions, finalJobIDS):
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    IDList = ''
    for i in finalJobIDS:
        IDList += ':' + str(i)

    command = 'sbatch -J EZMAP-FINALRESULTS -p '+configOptions['slurm-partition']+' --dependency=afterany:' + IDList[1:] + ' --wrap="'+configOptions['python3-path'] + ' ' + cwd + 'Scripts/gatherResults.py ' + projDir + ' ' + projName+'"'
    os.system(command)
