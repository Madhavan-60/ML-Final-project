@echo off
echo ====================================================================
echo   TRAFFIC MONITORING SYSTEM - WEB INTERFACE
echo ====================================================================
echo.
echo Starting server...
echo.
echo Your browser will open automatically at:
echo   http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo ====================================================================
echo.

cd /d "%~dp0"
start http://localhost:5000
C:/Users/LENOVO/AppData/Local/Programs/Python/Python310/python.exe app.py

pause
