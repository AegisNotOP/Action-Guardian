@echo off
title ActionGuardian - Cognition 2026
echo ========================================================
echo  Starting ActionGuardian Simulation Dashboard...
echo ========================================================
echo.
cd /d "%~dp0"
echo Opening browser to http://localhost:8000 ...
start http://localhost:8000
python app.py
pause
