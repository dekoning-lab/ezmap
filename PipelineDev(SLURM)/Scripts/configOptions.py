__author__ = 'patrickczeczko'

import os


def parseConfigOptions():
    cwd = os.getcwd() + '/'
    configFile = open(cwd + 'param.config', 'r')

    configOptions = {}
    for line in configFile:
        if line.startswith('#'):
            option = line.split('=')
            option[1] = option[1].replace('\n', '')
            configOptions[option[0][1:]] = option[1]
    return configOptions
