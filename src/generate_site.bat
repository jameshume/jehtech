@echo off
python generate_site.py
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" file://%~dp0..\__deployed\index.html
pause
