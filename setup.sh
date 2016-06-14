#!/usr/bin/env bash

echo "Installing EzMap dependencies..."
# Setup Script to install all required dependencies
echo "Current Python Version Installed"
python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'

# Check to see if NumPy is installed
echo "Checking for NumPy installation..."
if pip3 list | grep numpy; then
	echo "NumPy already installed..."
else
	echo "Installing NumPy..."
    pip3 install numpy
fi

# Check to see if SciPy is installed
echo "Checking for SciPy installation..."
if pip3 list | grep scipy; then
	echo "SciPy already installed..."
else
	echo "Installing SciPy..."
    pip3 install scipy
fi

# Check to see if Biopython is installed
echo "Checking for Biopython installation..."
if pip3 list | grep biopython; then
	echo "Biopython already installed..."
else
	echo "Installing Biopython..."
    pip3 install biopython
fi

# Download hg19 image
echo "Downloading hg19 files for Bowtie2"
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
rm hg19.zip

echo "Done... Please check for any error messages listed above"



