@echo off
echo ====================================
echo  Splay Setup (No Docker Required!)
echo ====================================
echo.

REM Navigate to API directory
cd apps\api

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Running database migrations...
alembic upgrade head

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To start the server, run:
echo   cd apps\api
echo   venv\Scripts\activate
echo   python run.py
echo.
echo Then open: http://localhost:8000
echo.
pause
