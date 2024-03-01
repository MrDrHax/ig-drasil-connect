#!/bin/bash

# Check if pyenv is installed
if ! command -v python3 -m venv &> /dev/null
then
    echo "pyenv could not be found, please install it first: Trying to run: python3 -m venv apienv"
    sudo apt install python3.10-venv -y
    exit
fi

# Create a new virtual environment
python3 -m venv connectEnv

# Activate the virtual environment
source connectEnv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the dependencies
pip install -r requirements.txt