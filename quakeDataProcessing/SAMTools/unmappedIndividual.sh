#!/bin/bash
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=unmappedCollections
#SBATCH --workdir=/hyperion/work/patrick/quakeDataMapping/
#SBATCH --output=unmappedCollections-%j.out
#SBATCH --error=unmappedCollections-%j.err
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

inFileDir=/hyperion/work/patrick/quakeDataMapping/SAM/
outFileDir=/hyperion/work/patrick/quakeDataMapping/unmappedSAM/
samtoolsPath=/hyperion/work/patrick/quakeDataMapping/samtools-1.2/samtools

fileArray=($(python unmapped.py ${inFileDir} | tr -d '[],'))

start=$(date +%s.%N)

echo "Start time: ${start}"

#Grab array of COMMANDs from parent shell
FILE=${fileArray[${SLURM_ARRAY_TASK_ID}]}

TEMP=${FILE#\'}
TEMP2=${TEMP%\'}
TEMP3=${TEMP2:0:10}

echo "Processing: $TEMP3"

${samtoolsPath} view -f4 $inFileDir$TEMP2 > $outFileDir$TEMP3.unmapped.sam

#echo "File: ${TEMP3}"
#echo "converting to bam..."
#${samtoolsPath} view -bS $inFileDir$TEMP2 > $TEMP3.bam
#echo "sorting..."
#${samtoolsPath} sort $TEMP3.bam -o $TEMP3.sorted.bam -O bam -T out.bam
#echo "indexing..."
#${samtoolsPath} index $TEMP3.sorted.bam
#echo "finding unmapped reads..."
#${samtoolsPath} view -b -f 4 $TEMP3.sorted.bam > $TEMP3.unmapped.bam
#
#${samtoolsPath} view $TEMP3.unmapped.bam > $TEMP3.unmapped.sam
#
#echo "complete..."

end=$(date +%s.%N)
echo "End time: ${end}"

runtime=$(python -c "print(${end} - ${start})")

echo "Runtime was $runtime seconds"