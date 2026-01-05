# launch_selector.ps1
# Quick launcher for Domain & Topic Selector UI

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Domain & Topic Selector - Quick Launcher" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if server is already running
$serverRunning = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*domain_selector_server*"}

if (-not $serverRunning) {
    Write-Host "Starting server..." -ForegroundColor Yellow
    Start-Process python -ArgumentList "domain_selector_server.py" -WindowStyle Hidden
    Start-Sleep -Seconds 2
    Write-Host "Server started on http://localhost:8000" -ForegroundColor Green
} else {
    Write-Host "Server already running on http://localhost:8000" -ForegroundColor Green
}

Write-Host ""
Write-Host "Opening UI in browser..." -ForegroundColor Yellow
Start-Process "domain_selector_ui.html"

Write-Host ""
Write-Host "Done! UI should now be open in your browser." -ForegroundColor Green
Write-Host ""
Write-Host "To stop the server later, run: Stop-Process -Name python -Force" -ForegroundColor Gray
