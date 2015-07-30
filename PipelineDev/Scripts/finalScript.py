__author__ = 'patrickczeczko'
import subprocess, os
import Scripts.slurmScript as slurmScript


def collectPipelineResult(projdir, configOptions, finalJobIDS):
    cwd = os.path.dirname(os.path.abspath(__file__)).strip('Scripts')

    script = open(projdir + '6-FinalResult/resultsScript.sh', 'w+')

    slurmScript.getSBATCHSettings(script, 6, projdir + '6-FinalResult/', configOptions)

    IDList = ''
    for i in finalJobIDS:
        IDList += ':' + str(i)
    script.write('#SBATCH --dependency=afterany:' + IDList[1:] + '\n\n')

    script.write('/cm/shared/apps/python3.4/bin/python3 ' + cwd + 'Scripts/gatherResults.py ' + projdir)

    proc = subprocess.Popen(
        ['sbatch', projdir + '6-FinalResult/resultsScript.sh'], stdout=subprocess.PIPE)
