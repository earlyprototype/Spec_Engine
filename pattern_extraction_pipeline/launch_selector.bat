@echo off
REM launch_selector.bat
REM Quick launcher for Domain & Topic Selector UI

echo ======================================================================
echo Domain ^& Topic Selector - Quick Launcher
echo ======================================================================
echo.

echo Starting server...
start /B python domain_selector_server.py
timeout /t 2 /nobreak >nul

echo Opening UI in browser...
start domain_selector_ui.html

echo.
echo Done! UI should now be open in your browser.
echo Server running on http://localhost:8000
echo.
pause
