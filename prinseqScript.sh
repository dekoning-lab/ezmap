#!/bin/bash
#!/usr/bin/perl
#SBATCH --job-name=JobName
#SBATCH --output=res.txt
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100
#

## Directory Containing Files to Process
dirPath= $1

## PRINSEQ PARAMETERS
out_format=3
min_qual_score=1
lc_method="dust"
lc_threshold=7

## For each file in directory clean the files 
## based on above parameters
for file in $( find $dirPath*.fastq -maxdepth 1 -type f  ); 
do
	perl prinseq-lite.pl -fastq $file -out_format $out_format -log  -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold
done
     



