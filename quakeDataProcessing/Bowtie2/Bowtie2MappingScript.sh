#!/bin/bash
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=bowtie2Mapping4core
#SBATCH --workdir=/hyperion/work/patrick/quakeDataMapping/
#SBATCH --output=bowtie2Mapping-%j.out
#SBATCH --error=bowtie2Mapping-%j.errs
#SBATCH --account=dklab-research

# Resources required
#SBATCH --ntasks=1
#SBATCH --ntasks-per-socket=2
#SBATCH --share

# Optional settings (uncomment required)
#SBATCH --partition=normal

numCores=4

fileArray=($(python errorCheck.py | tr -d '[],'))

#!/bin/bash
start=$(date +%s.%N)

echo "Start time: ${start}"

#Grab array of filenames from parent shell
FILENAME=${fileArray[${SLURM_ARRAY_TASK_ID}]}

TEMP=${FILENAME#\'}
TEMP2=${TEMP%\'}

echo "Input file: ${TEMP2}"
/hyperion/work/patrick/quakeDataMapping/bowtie2-2.2.5/bowtie2 --sensitive -x hg19 -U /hyperion/work/patrick/quake-data/prinseqResults-minQual21/${TEMP2} -S ${TEMP2}.sam -p ${numCores}

end=$(date +%s.%N)
echo "End time: ${end}"

runtime=$(python -c "print(${end} - ${start})")

echo "Runtime was $runtime seconds"

