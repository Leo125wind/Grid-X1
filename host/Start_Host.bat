@echo off
TITLE Grid-X Host Node
COLOR 0A

REM --- CRITICAL FIX: Force script to run from its own folder ---
cd /d "%~dp0"

echo ===================================================
echo      GRID-X HOST SETUP (ONE-CLICK)
echo ===================================================
echo.

REM 1. SECURITY CHECK: Did they update the IP?
REM We look for the default localhost string.
findstr /C:"REGISTRY_URL = \"http://127.0.0.1:5000\"" gridx_service.py >nul
if %errorlevel% equ 0 goto :IP_ERROR

REM 2. CHECK PYTHON
python --version >nul 2>&1
if %errorlevel% neq 0 goto :PYTHON_ERROR

REM 3. CHECK DOCKER
docker info >nul 2>&1
if %errorlevel% neq 0 goto :DOCKER_ERROR

REM 4. INSTALL DEPENDENCIES
if not exist "installed.flag" (
    echo [*] First run detected. Installing libraries...
    pip install -r requirements_host.txt
    if %errorlevel% neq 0 goto :PIP_ERROR
    echo done > installed.flag
)

REM 5. BUILD CONTAINER
echo [*] verifying Grid-X Secure Container Image...
docker build -t gridx-secure-unit .
if %errorlevel% neq 0 goto :BUILD_ERROR

REM 6. START SERVICE
echo.
echo [*] Starting Service...
echo     (Look for the Green Icon in your System Tray)
echo.
python gridx_service.py

REM If python crashes or closes, we go here
goto :END

REM ---------------------------------------------------
REM ERROR HANDLERS (The "Safety Net")
REM ---------------------------------------------------

:IP_ERROR
COLOR 0C
echo.
echo [CRITICAL ERROR] CONFIGURATION MISSING!
echo ---------------------------------------------------
echo You are trying to connect to '127.0.0.1' (Localhost).
echo This will NOT work for other users.
echo.
echo ACTION REQUIRED:
echo 1. Right-click 'gridx_service.py' -> Edit.
echo 2. Find the line: REGISTRY_URL = "..."
echo 3. Replace '127.0.0.1' with the Admin's Public URL.
echo    (Example: http://5a2b.ngrok-free.app)
echo ---------------------------------------------------
goto :END

:PYTHON_ERROR
COLOR 0C
echo.
echo [ERROR] Python is not installed or not in your PATH.
echo Please install Python 3.x from python.org.
goto :END

:DOCKER_ERROR
COLOR 0C
echo.
echo [ERROR] Docker is not running!
echo Please open 'Docker Desktop' and wait for the engine to start.
goto :END

:PIP_ERROR
COLOR 0C
echo.
echo [ERROR] Failed to install dependencies.
echo Check your internet connection.
goto :END

:BUILD_ERROR
COLOR 0C
echo.
echo [ERROR] Docker build failed.
echo Check the error message above.
goto :END

:END
echo.
echo Press any key to close...
pause >nul