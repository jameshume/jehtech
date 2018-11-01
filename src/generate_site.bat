@echo off
python generate_site.py %1%
IF %ERRORLEVEL% EQU 0 "%~dp0..\__deployed\index.html"
pause
