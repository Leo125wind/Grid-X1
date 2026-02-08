@echo off
TITLE Grid-X Client Terminal
COLOR 0E
cd /d "%~dp0"

echo ===================================================
echo      GRID-X CLIENT PORTAL
echo ===================================================
echo.

REM 1. Install Dependencies
if not exist "installed.flag" (
    echo [*] Installing dependencies...
    pip install -r requirements_client.txt
    echo done > installed.flag
)

REM 2. Launch Client Script
python tenant.py

pause