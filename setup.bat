@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   ABC Vault Bot - First-time setup
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo Python was not found on this computer.
    echo.
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.10 or newer
    echo 3. During install, check "Add python.exe to PATH"
    echo 4. Run this setup.bat again
    echo.
    pause
    exit /b 1
)

echo Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

if not exist "config.yaml" (
    copy /Y "config.example.yaml" "config.yaml" >nul
    echo.
    echo Created config.yaml from the example file.
    echo Open config.yaml in Notepad and add your ABC login, Vault key, and keywords.
    echo See SETUP.md for step-by-step instructions.
) else (
    echo config.yaml already exists - left unchanged.
)

echo.
echo Setup complete. Edit config.yaml, then double-click run.bat on Vault day.
echo.
pause
