# This script is designed to allow for large FASTQ files to processed by PRINSEQ in a chunked manner
# Command line variables:
# $1 = the directory containing the input file
# $2 = the name of the file ex: SRR1024.fastq
# $3 = the directory to place results in
# $4 = the path to the directory containing both prinseq and fastq-splitter
# $5 = the number of threads to use to process the file
# $6 = the format that the prinseq output shoudl be in
# $7 = the prinseq min_qaual_score
# $8 = the prinseq lc_method
# $9 = the prinseq lc_thereshold

#!/bin/bash

inputDIR=$1
FILE=$2
outputDIR=$3
TOOLSDIR=$4
numParts=$5

out_format=$6 #3
min_qual_score=$7 #21
lc_method=$8 #dust
lc_threshold=$9 #7
pythonPath=${10}
prinseqPath=${11}

echo "Splitting ${FILE} into ${numParts} parts..."
# Split the fastq file into the number of threads to process with
${pythonPath} ${prinseqPath}splitFASTQ.py ${inputDIR}${FILE} ${numParts}

COUNTER=1

inputFileName="${FILE%.*}"

 For each piece of the original fastq process using prinseq
for fullfile in ${inputDIR}${inputFileName}.part*.fastq; do
    echo "Cleaning each part of the original file..."

    filename=$(basename "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"

    echo "perl ${prinseqPath}prinseq-lite.pl -fastq ${fullfile} -out_format $out_format -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold -log -out_good ${outputDIR}${filename}-prinseq -out_bad null"

    if [ $COUNTER == $numParts ] ; then
        perl ${prinseqPath}prinseq-lite.pl -fastq ${fullfile} -out_format $out_format -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold -log -out_good ${outputDIR}${filename}-prinseq -out_bad null
    else
        perl ${prinseqPath}prinseq-lite.pl -fastq ${fullfile} -out_format $out_format -min_qual_score $min_qual_score -lc_method $lc_method -lc_threshold $lc_threshold -log -out_good ${outputDIR}${filename}-prinseq -out_bad null &
    fi

    let COUNTER=COUNTER+1
done

wait

echo "Combining results..."
echo "cat ${outputDIR}${inputFileName}*.part*-prinseq.fastq > ${outputDIR}${inputFileName}-prinseq.fastq"

cat ${outputDIR}${inputFileName}*.part*-prinseq.fastq > ${outputDIR}${inputFileName}-prinseq.fastq

# Combine the results of the prinseq log files
${pythonPath} ${prinseqPath}combineLogFiles.py ${outputDIR}${inputFileName}-prinseq.fastq.log echo ${inputDIR}*part*.log

echo "Removing temporary files..."
# Remove unnecessary part files
rm ${inputDIR}${inputFileName}*.part*
rm ${outputDIR}${inputFileName}*.part*.fastq

wait

echo "Done...!"