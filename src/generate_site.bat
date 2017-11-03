@echo off
python generate_site.py %1%
"%~dp0..\__deployed\index.html"
pause
