

fileArray=($(python missingFiles.py | tr -d '[],'))

numOfFiles=${#fileArray[@]}

echo ${numOfFiles}

#sbatch --array=0-${#fileArray[@]} prinseqIndividualScript.sh

