@echo off
title Lugs Reader Launcher
echo === Starting Discord Lugs Reader System ===

set "LNK_NAME=Discord Lugs Reader.lnk"
set "EXE_NAME=venv311_new\Scripts\python.exe"
set "SCRIPT_NAME=main.py"
set "WATCHER_SCRIPT=ocr_watcher.py"
set "ICON_NAME=DLR.ico"

cd /d "%~dp0"

echo [1/3] Checking files...
if not exist "%SCRIPT_NAME%" (
    echo [ERROR] %SCRIPT_NAME% not found!
    pause
    exit /b
)
if not exist "%WATCHER_SCRIPT%" (
    echo [ERROR] %WATCHER_SCRIPT% not found!
    pause
    exit /b
)

echo [2/3] Starting OCR Engine (Background)...
start "" /MIN "%EXE_NAME%" "%WATCHER_SCRIPT%"

echo [3/3] Launching Main Application...
REM Create shortcut with icon
set "PS_CMD=$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%~dp0%LNK_NAME%'); $s.TargetPath = '%~dp0%EXE_NAME%'; $s.Arguments = '%~dp0%SCRIPT_NAME%'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0%ICON_NAME%'; $s.Save()"
powershell -Command "%PS_CMD%"

REM Launch the shortcut
start "" "%LNK_NAME%"

echo.
echo System started successfully! 
echo You can close this window, or it will close automatically.
timeout /t 5 >nul
exit
