@echo off
echo ============================================
echo Amazon Knowledge Support System
echo ============================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10 or higher
    pause
    exit
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Run setup first
    pause
    exit
)

echo.
echo Starting application...
echo.
echo Access the system at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause