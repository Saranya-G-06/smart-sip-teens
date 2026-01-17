@echo off
echo ========================================
echo   🚀 FINSTRIDE - Teen Financial App
echo ========================================
echo.
echo Starting your financial journey...
echo.

echo Creating necessary directories...
mkdir users 2>nul
mkdir users\avatars 2>nul
mkdir data 2>nul
mkdir models 2>nul

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting the application...
echo.
echo 🌐 Open in browser: http://localhost:8501
echo 📱 Mobile friendly interface
echo 🔒 Secure local data storage
echo.
echo ========================================
echo.

streamlit run app_pro.py
pause