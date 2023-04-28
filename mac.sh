#!/bin/bash

set -e

# Define color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

venv_path="./src/venv"
requirements_path="./src/requirements.txt"

# Check if Homebrew is installed
if ! [ -x "$(command -v brew)" ]; then
  echo -e "${RED}Homebrew is not installed. Installing Homebrew...${NC}"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check if Python 3 is installed
if ! [ -x "$(command -v python3)" ]; then
  echo -e "${RED}Python 3 is not installed. Installing Python 3...${NC}"
  brew install python3
fi

echo -e "${GREEN}Checking virtual environment...${NC}"
if [[ ! -d "$venv_path" ]]
then
    echo -e "${RED}Virtual environment not found. Creating it now...${NC}"
    python3 -m venv $venv_path || { echo -e "${RED}Error creating virtual environment.${NC}"; exit 1; }
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

echo -e "${GREEN}Activating virtual environment...${NC}"
source "$venv_path/bin/activate" || { echo -e "${RED}Error activating virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment activated.${NC}"

if [[ ! -f "$requirements_path" ]]; then
    echo -e "${GREEN}Creating requirements.txt...${NC}"
    echo "openai==0.27.0" > $requirements_path
    echo "pyperclip==1.8.2" >> $requirements_path
    echo "Requests==2.29.0" >> $requirements_path
    echo "PyQt6==6.5.0" >> $requirements_path
    echo -e "${GREEN}requirements.txt created.${NC}"
fi

echo -e "${GREEN}Installing required packages...${NC}"
pip3 install -r src/requirements.txt || { echo -e "${RED}Error installing required packages.${NC}"; exit 1; }
echo -e "${GREEN}Packages installed.${NC}"

echo -e "${GREEN}Running the main script...${NC}"
python3 src/main.py || { echo -e "${RED}Error running main script.${NC}"; exit 1; }

echo -e "${GREEN}Deactivating virtual environment...${NC}"
deactivate || { echo -e "${RED}Error deactivating virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment deactivated.${NC}"
