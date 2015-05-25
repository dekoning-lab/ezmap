#!/bin/bash
#!/usr/bin/perl
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=prinseq
#SBATCH --workdir=/hyperion/work/patrick/quake-data/
#SBATCH --output=prinseq-%j.out
#SBATCH --error=prinseq-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

## DEFAULT PRINSEQ PARAMETERS
out_format=3
min_qual_score=33
lc_method="dust"
lc_threshold=7

while getopts f:q:m:t: opt; do
  case $opt in
  f)
      out_format=$OPTARG
      ;;
  q)
      min_qual_score=$OPTARG
      ;;
  m)
      lc_method=$OPTARG
      ;;
  t)
      lc_threshold=$OPTARG
      ;;
  esac
done

shift $((OPTIND - 1))

#fileArray=($(python missingFiles.py | tr -d '[],'))

#echo ${fileArray[@]}

#Grab array of filenames from parent shell
FILENAME=${fileArray[$SLURM_ARRAY_TASK_ID]}

TEMP=${FILENAME#\'}
TEMP2=${TEMP%\'}

echo $TEMP2

perl -w prinseq-lite.pl -fastq ${TEMP2} -out_format ${out_format} -log  -min_qual_score {$min_qual_score} -lc_method {$lc_method} -lc_threshold {$lc_threshold}