@echo off
echo DEPOLYING SITE....
echo ------------------
set /p pass="Enter password: "
python deploy_site.py %pass%
pause
