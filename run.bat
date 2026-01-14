@echo off
title IP-TOOL Launcher
cd /d "%~dp0"

echo 0101010101010010101010101010
echo        IP-TOOL RUNNER
echo 0101010101010010101010101010
echo.

REM
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not added to PATH.
  echo Install Python from python.org and enable "Add Python to PATH".
  pause
  exit /b 1
)

REM
if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creating virtual environment in ".venv"...
  python -m venv .venv
)

REM
echo [INFO] Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt

REM
echo.
echo [INFO] Starting IP-TOOL...
".venv\Scripts\python.exe" IP_lookup.py

echo.
echo [INFO] Program closed.
pause