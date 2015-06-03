#!/bin/sh
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=compress
#SBATCH --workdir=/hyperion/work/patrick/quake-data/originalData/
#SBATCH --output=compress-%j.out
#SBATCH --error=compress-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --ntasks-per-socket=1
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

for file in $(ls *.fastq); 
	do pigz-2.3.3/pigz -v -p 16 $file; 
done;

