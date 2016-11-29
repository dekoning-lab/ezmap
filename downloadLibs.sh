#!/usr/bin/env bash

# Download hg19 image

case $( uname -s ) in
Linux)  echo Linux

        echo "Downloading BLAST+ 2.4.0 files"
        wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast%2B/2.4.0/ncbi-blast-2.4.0%2B-x64-linux.tar.gz
        tar -xzf ncbi-blast-2.4.0+-x64-linux.tar.gz -C tools/BLAST/

        if [ -z "$1" ]
          then
            echo "Downloading both HISAT2 and BowTie2 Indexes for Hg19"

            wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/hg19.tar.gz
            tar -xvf hg19.tar.gz -C tools/HISAT2

            wget ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip
            mkdir tools/BOWTIE2/hg19
            unzip hg19.zip -d tools/BOWTIE2/hg19

        elif [ $1 == "HISAT2" ]
          then
            echo "Downloading HISAT2 Index for Hg19"

            wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/hg19.tar.gz
            tar -xvf hg19.tar.gz -C tools/HISAT2

        elif [ "$1" -eq "BWT2" ]
          then
            echo "Downloading BowTie2 Index for Hg19"

            wget ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip
            mkdir tools/BOWTIE2/hg19
            unzip hg19.zip -d tools/BOWTIE2/hg19

        fi
        ;;

Darwin) echo Darwin
        echo "Downloading hg19 files"
        curl -O ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip
        mkdir tools/BOWTIE2/hg19
        unzip hg19.zip -d tools/BOWTIE2/hg19

        echo "Downloading BLAST+ 2.4.0 files"
        curl -O ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast%2B/2.4.0/ncbi-blast-2.4.0%2B-x64-linux.tar.gz
        tar -xzf ncbi-blast-2.4.0+-x64-linux.tar.gz -C tools/BLAST/
        ;;

*)      echo other;;
esac
#rm hg19.zip
rm ncbi-blast-2.4.0+-x64-linux.tar.gz