@echo off

set VENV_PATH=./src/venv
set REQUIREMENTS_PATH=./src/requirements.txt

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed. Installing Python 3...
    choco install python
)

REM Check if virtual environment exists
if not exist %VENV_PATH% (
    echo Virtual environment not found. Creating it now...
    python -m venv %VENV_PATH% || (
        echo Error creating virtual environment.
        exit /b 1
    )
    echo Virtual environment created.
)

REM Activate virtual environment
call %VENV_PATH%\Scripts\activate.bat || (
    echo Error activating virtual environment.
    exit /b 1
)
echo Virtual environment activated.

REM Check if requirements file exists
if not exist %REQUIREMENTS_PATH% (
    echo Creating requirements.txt...
    echo openai==0.27.0 > %REQUIREMENTS_PATH%
    echo pyperclip==1.8.2 >> %REQUIREMENTS_PATH%
    echo requirements.txt created.
)

REM Install required packages
echo Installing required packages...
pip install -r src/requirements.txt || (
    echo Error installing required packages.
    exit /b 1
)
echo Packages installed.

REM Run the main script
echo Running the main script...
python src/main.py || (
    echo Error running main script.
    exit /b 1
)

REM Deactivate virtual environment
echo Deactivating virtual environment...
call %VENV_PATH%\Scripts\deactivate.bat || (
    echo Error deactivating virtual environment.
    exit /b 1
)
echo Virtual environment deactivated.
