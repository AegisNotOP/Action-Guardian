@echo off
title ActionGuardian - Cognition 2026
echo ========================================================
echo  Starting ActionGuardian Simulation Dashboard...
echo ========================================================
echo.
cd /d "%~dp0"
echo Opening browser to http://localhost:8000 ...
start http://localhost:8000
where python >nul 2>&1
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" app.py
) else (
    py app.py 2>nul || python app.py
)
pause
