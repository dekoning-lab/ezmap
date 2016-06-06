__author__ = 'patrickczeczko'
import os

def getSBATCHSettings(script, step, dir, configOptions):
    script.writelines(['#!/bin/bash\n',
                       '#!/usr/bin/perl\n',
                       '#---------------------------------\n',
                       '# Mandatory settings\n',
                       '#SBATCH --job-name=EZMAP-' + str(step) + '\n',
                       '#SBATCH --workdir=' + os.path.abspath(dir) + '\n',
                       '#SBATCH --output=EZMAP-' + str(step) + '-%j' + '.out\n',
                       '#SBATCH --error=EZMAP-' + str(step) + '-%j' + '.err\n',
                       '#SBATCH --account=' + configOptions['slurm-account'] + '\n\n',
                       '# Resources required\n',
                       '#SBATCH --ntasks=1\n',
                       '#SBATCH --nodes=1\n',
                       '#SBATCH --ntasks-per-node=2\n',
                       '#SBATCH --partition=' + configOptions['slurm-partition'] + '\n'])

    if configOptions['slurm-share'] == 'yes':
        script.write('#SBATCH --share\n')
    if configOptions['slurm-test-only'] == 'yes':
        script.write('#SBATCH --test-only\n')


