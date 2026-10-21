@echo off
setlocal
cd /d "%~dp0"

if not exist "config.yaml" (
    echo config.yaml not found.
    echo Run setup.bat first, then edit config.yaml with your settings.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\activate.bat" (
    echo Setup not finished. Double-click setup.bat first.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"
echo Starting ABC Vault Bot...
echo Press Ctrl+C to stop.
echo.
python -m abcvaultbot -c config.yaml
echo.
echo Bot stopped.
pause
