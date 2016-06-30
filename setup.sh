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

echo "Done... Please check for any error messages listed above"



