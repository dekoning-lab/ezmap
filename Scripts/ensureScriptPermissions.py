__author__ = 'patrickczeczko'

import os

def checkForScriptPermisions(configOptions):
    # Check for proper PRINSEQ permissions ---------------------
    cwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)).strip('Scripts'))
    prinseqPath = configOptions['prinseq-path']

    # Checks to see if path ends in / character
    if not prinseqPath.endswith('/'):
        prinseqPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/PRINSEQ/' in prinseqPath:
        prinseqPath = prinseqPath.replace('cwd', cwd)

    os.chmod(prinseqPath + 'combineLogFiles.py', 0o755)
    os.chmod(prinseqPath + 'fastq-splitter.pl', 0o755)
    os.chmod(prinseqPath + 'prinseq-lite.pl', 0o755)
    os.chmod(prinseqPath + 'prinseqMultipleThread.sh', 0o755)

    # Check for proper BOWTIE2 permissions ---------------------
    bowtie2Path = configOptions['bowtie2-path']

    # Checks to see if path ends in / character
    if not bowtie2Path.endswith('/'):
        bowtie2Path += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BOWTIE2/' in bowtie2Path:
        bowtie2Path = bowtie2Path.replace('cwd', cwd)

    for file in os.listdir(bowtie2Path):
        if 'bowtie2' in file:
            os.chmod(bowtie2Path + file, 0o755)

    # Check for proper SAMTOOLS permissions ---------------------
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    samtoolsPath = configOptions['samtools-path']

    # Checks to see if path ends in / character
    if not samtoolsPath.endswith('/'):
        samtoolsPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/SAMTOOLS/' in samtoolsPath:
        samtoolsPath = samtoolsPath.replace('cwd', cwd)

    os.chmod(samtoolsPath + 'samtools', 0o755)

    # Check for proper BLAST permissions ---------------------

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    blastPath = configOptions['blast-path']

    # Checks to see if path ends in / character
    if not blastPath.endswith('/'):
        blastPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/BLAST/' in blastPath:
        blastPath = blastPath.replace('cwd', cwd)

    os.chmod(cwd + '/tools/BLAST/BLASTWithHitFilter.py', 0o755)

    # Check for proper EMAL permissions ---------------------

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    emalPath = configOptions['emal-path']

    # Checks to see if path ends in / character
    if not emalPath.endswith('/'):
        emalPath += '/'

    # Checks to see if default path should be used
    if 'cwd/tools/EMAL/' in emalPath:
        emalPath = emalPath.replace('cwd', cwd)

    os.chmod(emalPath + 'EMAL-DataPrep.py', 0o755)
    os.chmod(emalPath + 'EMAL-Main.py', 0o755)
    os.chmod(emalPath + 'EMAL-Post.py', 0o755)

    print('File permissions for scripts verified ...')

