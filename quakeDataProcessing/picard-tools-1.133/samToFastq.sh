#!/bin/bash
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=SAMToFASTQ
#SBATCH --workdir=/hyperion/work/patrick/quakeDataProcessing/picard-tools-1.133/
#SBATCH --output=SAMToFASTQ-%j.out
#SBATCH --error=SAMToFASTQ-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --tasks-per-node=1
#SBATCH --mem=3072
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

inFileDir=/hyperion/work/patrick/quakeData/unmappedSAM/
outFileDir=/hyperion/work/patrick/quakeData/unmappedFASTQ/
picardtoolsPath=/hyperion/work/patrick/quakeDataProcessing/picard-tools-1.133/picard.jar

fileArray=($(python fileListGenerator.py ${inFileDir} | tr -d '[],'))

start=$(date +%s.%N)

echo "Start time: ${start}"

#Grab array of COMMANDs from parent shell
FILE=${fileArray[${SLURM_ARRAY_TASK_ID}]}

TEMP=${FILE#\'}
TEMP2=${TEMP%\'}
TEMP3=${TEMP2:0:10}

echo "Processing: $TEMP3"

java -jar ${picardtoolsPath} SamToFastq INPUT=${inFileDir}${TEMP2} FASTQ=${outFileDir}${TEMP3}.fastq

end=$(date +%s.%N)
echo "End time: ${end}"

runtime=$(python -c "print(${end} - ${start})")

echo "Runtime was $runtime seconds"


