p#Grab the files and export so that child sbatch can use
#export FILES=($(ls -1 *.fastq))

#get size of array
#NumFASTQ=${#FILES[@]}

#subtract 1
#ZerobaseNumFASTQ=$(($NumFASTQ - 1))

#if [ $ZerobaseNumFASTQ -ge 0 ]; then

#sbatch --array=0-$ZerobaseNumFASTQ prinseqIndividualScript.sbatch

#fi

fileArray=($(python missingFiles.py | tr -d '[],'))

numOfFiles=${#fileArray[@]}

echo ${numOfFiles}

sbatch --array=0-${#fileArray[@]} prinseqIndividualScript.sbatch

#for FILE in *.fastq; do
	#echo ${FILE}
	#sbatch prinseqIndividualScript.sbatch ${FILE}
#done
