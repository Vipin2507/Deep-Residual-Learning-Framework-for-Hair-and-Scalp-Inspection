@echo off
title Hair & Scalp Disease Prediction System
color 0A

echo ============================================================
echo   HAIR ^& SCALP DISEASE PREDICTION SYSTEM
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version
echo.

REM Check if virtual environment exists
if not exist "minor\.venv" (
    echo Creating virtual environment...
    cd minor
    python -m venv .venv
    cd ..
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment and install requirements
echo Installing/Updating dependencies...
cd minor
call .venv\Scripts\activate.bat

REM Install requirements
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo ============================================================
echo   LAUNCHING APPLICATION...
echo ============================================================
echo.

REM Go back to root and run the launcher
cd ..
python run_app.py

pause
