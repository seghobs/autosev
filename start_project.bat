@echo off
REM Flask Project Starter for Windows
REM Usage: start_project.bat <python_path> <project_file>

set PYTHON_EXE=%1
set PROJECT_FILE=%2
set PROJECT_DIR=%~dp2

echo ========================================
echo  Flask Project Launcher
echo ========================================
echo Python: %PYTHON_EXE%
echo File: %PROJECT_FILE%
echo Dir: %PROJECT_DIR%
echo ========================================
echo.

cd /d "%PROJECT_DIR%"

REM Disable reloader for Windows
set WERKZEUG_RUN_MAIN=true
set FLASK_ENV=production

"%PYTHON_EXE%" "%PROJECT_FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] Program crashed!
    pause
)
