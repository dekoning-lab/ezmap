#!/bin/bash
#---------------------------------
# Hyperion/SLURM job-script

# Mandatory settings
#SBATCH --job-name=BLAST
#SBATCH --workdir=/hyperion/work/patrick/quakeDataProcessing/BLAST/
#SBATCH --output=BLAST-%j.out
#SBATCH --error=BLAST-%j.err
#SBATCH --account=dklab-research

# Resources required
##SBATCH --distribution arbitrary
##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --tasks-per-node=2
##SBATCH --test-only
#SBATCH --overcommit

# Optional settings (uncomment required)
#SBATCH --partition=normal

#  RM_HOSTFILE='/hyperion/work/patrick/quakeDataProcessing/BLAST/hostfile.txt'

job=$((${SLURM_ARRAY_TASK_ID}))
let job2=job+1

echo $job
echo $job2

BLASTPATH="/hyperion/work/patrick/quakeDataProcessing/BLAST/ncbi-blast-2.2.30+/bin/"
FILEPATH="/hyperion/work/patrick/quakeData/unmappedFASTQ/"
DBPATH="/hyperion/work/patrick/quakeDataProcessing/BLAST/ncbi-blast-2.2.30+/db/viral.1.1.genomic.fna"

fileArray=($(python unblasted.py ${FILEPATH} | tr -d '[],'))
FILENAME=${fileArray[${job}]}
FILENAME2=${fileArray[${job2}]}

TEMP=${FILENAME#\'}
TEMP2=${TEMP%\'}
TEMP3=${TEMP2:0:10}

TMP=${FILENAME2#\'}
TMP2=${TMP%\'}
TMP3=${TMP2:0:10}

start=$(date +%s.%N)

echo "Start time: ${start}"

echo -e "\nStarting BLAST on: ${TEMP2}\n"

perl -ne '$c++; if ($c==1){$_=~/\@(\S+)/; print ">$1\n"} if($c==2){print "$_"} if ($c==4){$c=0}' ${FILEPATH}${TEMP2} > ${TEMP3}".fasta"
perl -ne '$c++; if ($c==1){$_=~/\@(\S+)/; print ">$1\n"} if($c==2){print "$_"} if ($c==4){$c=0}' ${FILEPATH}${TMP2} > ${TMP3}".fasta"

cmd="${BLASTPATH}blastn -db ${DBPATH} -query ${TEMP3}".fasta" -task blastn -dust no -reward 1 -penalty -3 -word_size 12 -gapopen 5 -gapextend 2 -evalue 0.0001 -perc_identity 90 -culling_limit 2 -out ${TEMP3}.txt -outfmt 6 -num_threads 8"
cmd2="${BLASTPATH}blastn -db ${DBPATH} -query ${TMP3}".fasta" -task blastn -dust no -reward 1 -penalty -3 -word_size 12 -gapopen 5 -gapextend 2 -evalue 0.0001 -perc_identity 90 -culling_limit 2 -out ${TMP3}.txt -outfmt 6 -num_threads 8"

echo $cmd
echo $cmd2

#srun -m arbitrary -n 1 ${cmd}
srun ${cmd} &
srun ${cmd2}

end=$(date +%s.%N)
echo "End time: ${end}"

runtime=$(python -c "print(${end} - ${start})")

echo "Runtime was $runtime seconds"
