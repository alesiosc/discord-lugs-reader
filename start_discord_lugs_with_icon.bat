@echo off
set "LNK_NAME=Discord Lugs Reader.lnk"
set "EXE_NAME=venv311_new\Scripts\python.exe"
set "SCRIPT_NAME=main.py"
set "WATCHER_SCRIPT=ocr_watcher.py"
set "ICON_NAME=app_icon.ico"

cd /d "%~dp0"

if not exist "%SCRIPT_NAME%" (
    echo [ERROR] %SCRIPT_NAME% not found!
    echo Please ensure you are running this from the project root.
    pause
    exit /b
)

if not exist "%WATCHER_SCRIPT%" (
    echo [ERROR] %WATCHER_SCRIPT% not found!
    echo Please ensure you are running this from the project root.
    pause
    exit /b
)

REM Start OCR Watcher in the background (hidden)
echo [SETUP] Starting OCR Watcher...
start "" /MIN "%EXE_NAME%" "%WATCHER_SCRIPT%"

REM Create (or update) the shortcut to ensure it uses the custom icon
echo [SETUP] Creating taskbar-friendly launcher...
set "PS_CMD=$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%~dp0%LNK_NAME%'); $s.TargetPath = '%~dp0%EXE_NAME%'; $s.Arguments = '%~dp0%SCRIPT_NAME%'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0%ICON_NAME%'; $s.Save()"
powershell -Command "%PS_CMD%"

REM Launch the shortcut which spawns the window with the correct icon
echo [LAUNCH] Starting Application...
start "" "%LNK_NAME%"

REM Close this launcher script
exit
