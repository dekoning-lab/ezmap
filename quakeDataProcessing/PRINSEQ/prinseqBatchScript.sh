

fileArray=($(python missingFiles.py | tr -d '[],'))

numOfFiles=${#fileArray[@]}

echo ${numOfFiles}

sbatch --array=0-20 prinseqIndividualScript.sh

