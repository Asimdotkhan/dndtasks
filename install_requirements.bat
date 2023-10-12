@echo off
:: Check if requirements.txt file exists
if not exist requirements.txt (
    echo The requirements.txt file does not exist in this directory.
    exit /b 1
)

:: Install Python packages using pip from requirements.txt
pip install -r requirements.txt

:: Check if any of the installations failed
if %errorlevel% neq 0 (
    echo Installation failed. Please check the package names in requirements.txt and try again.
    pause
) else (
    echo All packages listed in requirements.txt have been successfully installed.
    pause
)
