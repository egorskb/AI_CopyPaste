@echo off

setlocal

REM Define color codes
set "GREEN=\033[0;32m"
set "RED=\033[0;31m"
set "NC=\033[0m" REM No Color

set "venv_path=.\src\venv"
set "requirements_path=.\src\requirements.txt"

REM Check if Python 3 is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Python 3 is not installed. Installing Python 3...%NC%
    choco install python --params "/InstallDir:C:\Python" -y
)

echo %GREEN%Checking virtual environment...%NC%
if not exist "%venv_path%" (
    echo %RED%Virtual environment not found. Creating it now...%NC%
    python -m venv %venv_path% || (echo %RED%Error creating virtual environment.%NC% & exit /b 1)
    echo %GREEN%Virtual environment created.%NC%
)

echo %GREEN%Activating virtual environment...%NC%
call "%venv_path%\Scripts\activate.bat" || (echo %RED%Error activating virtual environment.%NC% & exit /b 1)
echo %GREEN%Virtual environment activated.%NC%

if not exist "%requirements_path%" (
    echo %GREEN%Creating requirements.txt...%NC%
    echo openai^=^=0.27.0 > %requirements_path%
    echo pyperclip^=^=1.8.2 >> %requirements_path%
    echo requests^=^=2.29.0 >> %requirements_path%
    echo %GREEN%requirements.txt created.%NC%
)

echo %GREEN%Installing required packages...%NC%
pip install -r src\requirements.txt || (echo %RED%Error installing required packages.%NC% & exit /b 1)
echo %GREEN%Packages installed.%NC%

echo %GREEN%Running the main script...%NC%
python src\main.py || (echo %RED%Error running main script.%NC% & exit /b 1)

echo %GREEN%Deactivating virtual environment...%NC%
call "%venv_path%\Scripts\deactivate.bat" || (echo %RED%Error deactivating virtual environment.%NC% & exit /b 1)
echo %GREEN%Virtual environment deactivated.%NC%

endlocal
