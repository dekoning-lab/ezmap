#!/bin/bash
#!/usr/bin/perl
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings (uncomment required)
#SBATCH --job-name=prinseq
#SBATCH --workdir=/hyperion/scratch/YOUR-ACCOUNT-HERE
#SBATCH --output=prinseq-%j.out
#SBATCH --error=prinseq-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=64
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=16

## PRINSEQ PARAMETERS
out_format=3
min_qual_score=33
lc_method="dust"
lc_threshold=7

#Grab array of filenames from parent shell
FILENAME=${FILES[$SLURM_ARRAY_TASK_ID]}

perl prinseq-lite.pl -fastq ${FILENAME} -out_format $out_format -log  -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold



