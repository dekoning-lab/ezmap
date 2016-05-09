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