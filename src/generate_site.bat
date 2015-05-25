@echo off
python generate_site.py
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" ..\__deployed\index.html
pause