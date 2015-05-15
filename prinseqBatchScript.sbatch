#Grab the files and export so that child sbatch can use
export FILES=($(ls -1 *.fastq))

#get size of array
NumFASTQ=${#FILES[@]}

#subtract 1
ZerobaseNumFASTQ=$(($NumFASTQ - 1))

if [ $ZerobaseNumFASTQ -ge 0 ]; then

sbatch --array=0-$ZerobaseNumFASTQ prinseqScript.sbatch
fi
