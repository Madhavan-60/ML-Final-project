@echo off
REM Traffic Monitoring System - Quick Launcher
REM This batch file provides easy access to all system functions

:menu
cls
echo ====================================================================
echo     TRAFFIC MONITORING SYSTEM - ML Project
echo ====================================================================
echo.
echo     Select an option:
echo.
echo     1. Quick Test (Verify system is working)
echo     2. View Traffic Patterns
echo     3. Make Predictions
echo     4. Evaluate Model Performance
echo     5. Run Complete Pipeline
echo     6. Regenerate Dataset
echo     7. Retrain Model
echo     8. Start Web Server (localhost:5000)
echo     9. Exit
echo.
echo ====================================================================
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto visualize
if "%choice%"=="3" goto inference
if "%choice%"=="4" goto evaluate
if "%choice%"=="5" goto pipeline
if "%choice%"=="6" goto generate
if "%choice%"=="7" goto train
if "%choice%"=="8" goto webapp
if "%choice%"=="9" goto end

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:test
cls
echo Running Quick Test...
echo.
python traffic_monitoring\test.py
pause
goto menu

:visualize
cls
echo Analyzing Traffic Patterns...
echo.
python traffic_monitoring\visualize.py
pause
goto menu

:inference
cls
echo Making Predictions...
echo.
python traffic_monitoring\inference.py
pause
goto menu

:evaluate
cls
echo Evaluating Model Performance...
echo.
python traffic_monitoring\evaluate.py
pause
goto menu

:pipeline
cls
echo Running Complete Pipeline...
echo.
python traffic_monitoring\main.py
pause
goto menu

:generate
cls
echo Generating New Dataset...
echo.
python traffic_monitoring\data_generator.py
pause
goto menu

:train
cls
echo Training Model...
echo.
python traffic_monitoring\model.py
pause
goto menu

:webapp
cls
echo Starting Web Server...
echo.
echo ====================================================================
echo   Web Interface will open at: http://localhost:5000
echo   Press CTRL+C to stop the server
echo ====================================================================
echo.
python traffic_monitoring\app.py
pause
goto menu

:end
cls
echo.
echo Thank you for using Traffic Monitoring System!
echo.
timeout /t 2 >nul
exit
