#!/usr/bin/env bash
# Setup Script to install all required dependencies
echo "Current Python Version Installed"
python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'

pip3 install biopython
pip3 install scipy
pip3 install numpy

