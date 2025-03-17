@echo off
REM Ensure script runs from its directory
cd /d "%~dp0"

REM Install the required Python packages
python -m pip install --upgrade pip
python -m pip install customtkinter selenium tk

REM Start the Python script without a terminal
start "" pythonw "%~dp0webserver.py"

exit