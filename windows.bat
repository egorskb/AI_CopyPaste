@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Define color codes
set GREEN=[0;32m
set RED=[0;31m
set NC=[0m

set venv_path=./venv

REM Check if Python 3 is installed
where python >nul 2>nul || (
  echo !RED!Error: Python 3 is not installed.!NC!
  exit /b 1
)

echo !GREEN!Checking virtual environment...!NC!
if not exist %venv_path% (
    echo !RED!Virtual environment not found. Creating it now...!NC!
    python -m venv venv || (echo !RED!Error creating virtual environment.!NC! & exit /b 1)
    echo !GREEN!Virtual environment created.!NC!
)

echo !GREEN!Activating virtual environment...!NC!
call %venv_path%\Scripts\activate.bat || (echo !RED!Error activating virtual environment.!NC! & exit /b 1)
echo !GREEN!Virtual environment activated.!NC!

echo !GREEN!Installing required packages...!NC!
pip install -r requirements.txt || (echo !RED!Error installing required packages.!NC! & exit /b 1)
echo !GREEN!Packages installed.!NC!

echo !GREEN!Running the main script...!NC!
python main.py || (echo !RED!Error running main script.!NC! & exit /b 1)

echo !GREEN!Deactivating virtual environment...!NC!
call %venv_path%\Scripts\deactivate.bat || (echo !RED!Error deactivating virtual environment.!NC! & exit /b 1)
echo !GREEN!Virtual environment deactivated.!NC!
