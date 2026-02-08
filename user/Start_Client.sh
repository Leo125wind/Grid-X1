#!/bin/bash

# ANSI Color Codes for a CLI look
CYAN='\033[1;36m'
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}===================================================${NC}"
echo -e "${CYAN}        GRID-X CLIENT PORTAL (LINUX/MAC)         ${NC}"
echo -e "${CYAN}===================================================${NC}"
echo ""

# ---------------------------------------------------
# 1. CHECK PYTHON 3
# ---------------------------------------------------
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[CRITICAL] Python 3 is NOT installed!${NC}"
    echo "Please install it using your package manager."
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - macOS: brew install python3"
    exit 1
fi

# ---------------------------------------------------
# 2. INSTALL DEPENDENCIES (Auto-Fix)
# ---------------------------------------------------
# We check if a marker file exists. If not, we install.
if [ ! -f "installed.flag" ]; then
    echo -e "${YELLOW}[*] First run detected. Installing dependencies...${NC}"
    
    # Try installing packages. 
    # Note: On some modern Linux distros, this might warn about 'break-system-packages'.
    pip3 install -r requirements_client.txt --disable-pip-version-check
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Pip install failed.${NC}"
        echo "Try installing 'python3-requests' via your system package manager instead."
        exit 1
    fi
    
    touch installed.flag
    echo -e "${GREEN}[+] Dependencies installed successfully.${NC}"
    echo ""
fi

# ---------------------------------------------------
# 3. LAUNCH THE CLIENT
# ---------------------------------------------------
echo -e "${GREEN}[*] Launching Grid-X Client...${NC}"
python3 tenant.py