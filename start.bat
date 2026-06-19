@echo off
title Background Remover

echo ========================================
echo  Starting Background Remover...
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Launching the app...
echo.
echo 🌐 The browser window will open automatically.
echo ⚠️  DO NOT close this terminal window while the tool is running.
echo.
echo Press CTRL+C in this window to stop the tool.
echo.

python app.py

echo.
echo ========================================
echo  The tool has been stopped.
echo ========================================
pause