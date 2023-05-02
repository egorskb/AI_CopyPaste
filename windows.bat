@echo off

setlocal

REM Define color codes
set "GREEN=0A"
set "RED=0C"
set "NC=07"

set "venv_path=.\src\venv"
set "requirements_path=.\src\requirements.txt"
set "log_file=.\logs\win_terminal.txt"

REM Check if Python 3 is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    call :PrintColor %RED% "Python 3 is not installed. Installing Python 3..."
    powershell.exe -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'; Start-Process -FilePath '%TEMP%\python-installer.exe' -ArgumentList '/passive', 'InstallAllUsers=1', 'PrependPath=1' -Wait; Remove-Item '%TEMP%\python-installer.exe';"
    call :PrintColor %GREEN% "Python installed successfully."
)

call :PrintColor %GREEN% "Checking virtual environment..."
if not exist "%venv_path%" (
    call :PrintColor %RED% "Virtual environment not found. Creating it now..."
    python -m venv %venv_path% || (call :PrintColor %RED% "Error creating virtual environment." & exit /b 1)
    call :PrintColor %GREEN% "Virtual environment created."
)

call :PrintColor %GREEN% "Activating virtual environment..."
call "%venv_path%\Scripts\activate.bat" || (call :PrintColor %RED% "Error activating virtual environment." & exit /b 1)
call :PrintColor %GREEN% "Virtual environment activated."

if not exist "%requirements_path%" (
    call :PrintColor %GREEN% "Creating requirements.txt..."
    echo openai^=^=0.27.0 > %requirements_path%
    echo pyperclip^=^=1.8.2 >> %requirements_path%
    echo requests^=^=2.29.0 >> %requirements_path%
	echo PyQt6^=^=6.5.0 >> %requirements_path%
    call :PrintColor %GREEN% "requirements.txt created."
)

call :PrintColor %GREEN% "Installing required packages..."
pip install -r src\requirements.txt || (call :PrintColor %RED% "Error installing required packages." & exit /b 1)
call :PrintColor %GREEN% "Packages installed."

call :PrintColor %GREEN% "Running the main script..."
python src\main.py 2> %log_file% || (call :PrintColor %RED% "Error running main script. Check the log file for details." & exit /b 1)

call :PrintColor %GREEN% "Deactivating virtual environment..."
call "%venv_path%\Scripts\deactivate.bat" || (call :PrintColor %RED% "Error deactivating virtual environment." & exit /b 1)
call :PrintColor %GREEN% "Virtual environment deactivated."

endlocal

exit /b 0

REM Functions
:PrintColor
color %1
echo %~2
color %NC%
exit /b 0
