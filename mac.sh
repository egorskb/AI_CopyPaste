#!/bin/bash

set -e

# Define color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

venv_path="./venv"

# Check if Python 3 is installed
if ! [ -x "$(command -v python3)" ]; then
  echo -e "${RED}Error: Python 3 is not installed.${NC}" >&2
  exit 1
fi

echo -e "${GREEN}Checking virtual environment...${NC}"
if [[ ! -d "$venv_path" ]]
then
    echo -e "${RED}Virtual environment not found. Creating it now...${NC}"
    python3 -m venv venv || { echo -e "${RED}Error creating virtual environment.${NC}"; exit 1; }
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

echo -e "${GREEN}Activating virtual environment...${NC}"
source "$venv_path/bin/activate" || { echo -e "${RED}Error activating virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment activated.${NC}"

echo -e "${GREEN}Installing required packages...${NC}"
pip3 install -r requirements.txt || { echo -e "${RED}Error installing required packages.${NC}"; exit 1; }
echo -e "${GREEN}Packages installed.${NC}"

echo -e "${GREEN}Running the main script...${NC}"
python3 main.py || { echo -e "${RED}Error running main script.${NC}"; exit 1; }

echo -e "${GREEN}Deactivating virtual environment...${NC}"
deactivate || { echo -e "${RED}Error deactivating virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment deactivated.${NC}"
