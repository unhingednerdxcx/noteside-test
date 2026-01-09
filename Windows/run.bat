@echo off
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo This script is not running with elevated privileges. Restarting with administrator rights...
    powershell -Command "Start-Process cmd -ArgumentList '/c, \"%~f0%\"' -Verb runAs"
    exit
)
echo Running script with elevated privileges...

start "" python "C:\Users\nuhoh\Downloads\NotesIDE-master\Windows\app.py"
pause

