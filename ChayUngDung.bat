@echo off
chcp 65001 > nul
title HOC VIEN MBA - RUNNER APP
color 0A

echo ========================================================
echo   MBA - KHOI DONG HE THONG TINH CHI SO SINH HOC ONLINE
echo ========================================================
echo.

:: 1. Kiem tra thu vien Streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Dang cai dat thu vien Streamlit...
    pip install streamlit
)

:: 2. Ep duyet qua Google Chrome
set BROWSER_PATH=""
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set BROWSER_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set BROWSER_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set BROWSER_PATH="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

:: 3. Chay ung dung Streamlit
echo Dang khoi dong ung dung tren Google Chrome...
start "" %BROWSER_PATH% "http://localhost:8501"
python -m streamlit run TinhChiSoSucKhoeOnline.py --server.headless=true --server.port=8501

pause