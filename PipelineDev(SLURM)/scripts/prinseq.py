import os
import subprocess

projDir = ''




def runPRINSEQonFiles (dataset,projDir):
    for sample in dataset.samples:
        print()
        # PRINSEQ Command

        command = 'sbatch -'

        proc = subprocess.Popen()

