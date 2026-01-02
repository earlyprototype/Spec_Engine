@echo off
REM Charity Shop POS System - Launch Script (Batch)
REM Simple batch file wrapper for users without PowerShell execution policy set

echo ============================================================
echo Charity Shop POS System - Launcher
echo ============================================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check database
if exist "src\charity_pos.db" (
    echo [OK] Database found
) else (
    echo [INFO] Creating database...
    cd src
    python init_database.py
    cd ..
)

echo.
echo ============================================================
echo Default Login Credentials:
echo ============================================================
echo   Admin:     username='admin'     password='admin123'
echo   Volunteer: username='volunteer' password='volunteer123'
echo.
echo   WARNING: Change default passwords in production!
echo ============================================================
echo.
echo Launching application...
echo.

cd src
python main.py

cd ..
echo.
echo Application closed.
pause



