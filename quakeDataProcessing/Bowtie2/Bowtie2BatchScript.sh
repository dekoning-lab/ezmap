fileArray=($(python errorCheck.py | tr -d '[],'))

numOfFiles=${#fileArray[@]}
echo Starting Bowtie2 Processing
echo Number of Files: ${numOfFiles}

sbatch --array=0-$((numOfFiles-1)) Bowtie2MappingScript.sh