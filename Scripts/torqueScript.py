import os

def getPBSSettings(script, step, dir, configOptions):
    script.writelines(['#!/bin/bash\n',
                       '#!/usr/bin/perl\n',
                       '#---------------------------------\n',
                       '# Mandatory settings\n',
                       '#PBS -N EZMAP-' + str(step) + '\n',
                       '#PBS -o EZMAP-' + str(step) + '-$PBS_JOBID' + '.out\n',
                       '#PBS -e EZMAP-' + str(step) + '-$PBS_JOBID' + '.err\n',

                       '# Resources required\n',
                       '#PBS -q ' + configOptions['pbs-queue'] + '\n'])