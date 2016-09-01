@echo off
python generate_site.py
"%~dp0..\__deployed\index.html"
pause
