#!/bin/bash

fileArray=($(python unmapped.py /hyperion/work/patrick/quakeDataMapping/SAM  | tr -d '[],'))

numOfFiles=${#fileArray[@]}
echo Starting Bowtie2 Processing
echo Number of Files: ${numOfFiles/7}

sbatch --array=0-$((numOfFiles-1)) unmappedIndividual.sh

#sbatch --array=0-$((numOfFiles-1)) unmappedIndividual.sh