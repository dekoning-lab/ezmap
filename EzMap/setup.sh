#!/usr/bin/env bash

echo "Installing EzMap dependencies..."
# Setup Script to install all required dependencies
echo "Current Python Version Installed"
python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'

echo "Installing Biopython...\n"
pip3 install biopython

echo "Installing SciPy...\n"
pip3 install scipy

echo "Installing NumPy...\n"
pip3 install numpy

echo "Downloading hg19 files for Bowtie2\n"
case $( uname -s ) in
Linux)  echo Linux
        wget ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip
        mkdir tools/BOWTIE2/hg19
        unzip hg19.zip -d tools/BOWTIE2/hg19;;

Darwin) echo Darwin
        curl -O ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip
        mkdir tools/BOWTIE2/hg19
        unzip hg19.zip -d tools/BOWTIE2/hg19;;

*)      echo other;;
esac

