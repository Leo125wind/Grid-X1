@echo off
TITLE Grid-X Marketplace Server
COLOR 0B
cd /d "%~dp0"

echo ===================================================
echo      GRID-X REGISTRY SERVER
echo ===================================================
echo.

REM 1. Install Dependencies
if not exist "installed.flag" (
    echo [*] Installing dependencies...
    pip install -r requirements_registry.txt
    echo done > installed.flag
)

REM 2. Launch Registry
echo [*] Starting Web Dashboard...
echo [*] Edit gridx_service.py, section "REGISTRY_URL", to change the default registry address (http://localhost:5000) to the address below [*]
python registry.py

pause