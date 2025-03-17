#!/bin/bash

# Ensure the script runs from its directory
cd "$(dirname "$0")" || exit

# Check if python_stuff folder exists
if [ -d "python_stuff" ]; then
    echo "Folder exists, proceeding..."
else
    echo "Error: python_stuff folder does not exist!"
    exit 1
fi

# Install required Python packages
python3 -m pip install --upgrade pip
python3 -m pip install customtkinter selenium tk

# Change directory to python_stuff folder
cd python_stuff || exit

# Run the Python script
if [ -f "WebComplex.py" ]; then
    # Use "open" to run the Python script with python3
    open -a Terminal "python3 WebComplex.py"
else
    echo "Error: WebComplex.py not found!"
    exit 1
fi