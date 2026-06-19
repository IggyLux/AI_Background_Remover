@echo off
title Background Remover - Setup

echo ========================================
echo  Background Remover - Setup Wizard
echo ========================================
echo.

echo [1/4] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)
echo ✅ Python found!

echo.
echo [2/4] Creating virtual environment (venv)...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment created!

echo.
echo [3/4] Activating environment and installing packages...
echo (This will download ~120MB. Please wait...)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install packages. Check your internet connection.
    pause
    exit /b
)
echo ✅ Packages installed!

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo  You can now run "start.bat" to launch
echo  the Background Remover tool.
echo ========================================
echo.
pause