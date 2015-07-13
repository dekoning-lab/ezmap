#!/bin/bash
#!/usr/bin/perl
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=prinseq
#SBATCH --workdir=/hyperion/work/patrick/quake-data/originalData/
#SBATCH --output=prinseq-%j.out
#SBATCH --error=prinseq-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

## PRINSEQ PARAMETERS
out_format=3
min_qual_score=21
lc_method="dust"
lc_threshold=7

fileArray=($(python missingFiles.py | tr -d '[],'))

#echo ${fileArray[@]}

#Grab array of filenames from parent shell
TEMP=${fileArray[$SLURM_ARRAY_TASK_ID]}

TEMP2=${TEMP#\'}
FILENAME=${TEMP2%\'}

echo $TEMP2
#echo 'perl prinseq-lite.pl -fastq ${TEMP2} -out_format $out_format -log  -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold'
perl -w prinseq-lite.pl -fastq ${TEMP2} -out_format $out_format -log  -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold -out_bad null
