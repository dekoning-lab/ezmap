#!/usr/bin/env bash

FILES=/hyperion/work/patrick/quakeData/unmappedSAM/

numTotalReads=0

for f in $FILES
do
  echo "Processing $f file..."
  numReads=wc -l $f
  echo $numTotalReads
  $numTotalReads=$(numTotalReads+numReads)
done

echo $numTotalReads

