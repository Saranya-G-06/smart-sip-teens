@echo off
echo ========================================
echo  SMART SIP RECOMMENDATION SYSTEM
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Installing/Checking dependencies...
pip install -r requirements.txt

echo.
echo Starting the application...
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

streamlit run app.py
pause