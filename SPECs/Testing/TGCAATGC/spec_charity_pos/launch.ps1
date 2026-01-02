# Charity Shop POS System - Launch Script
# PowerShell script to check dependencies and launch the application

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Charity Shop POS System - Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "  ✓ Virtual environment found" -ForegroundColor Green
    Write-Host "  Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "  ℹ No virtual environment found (using system Python)" -ForegroundColor Yellow
}

# Check/install dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$requiredModules = @("sqlalchemy", "flask", "pytest")
$missingModules = @()

foreach ($module in $requiredModules) {
    try {
        python -c "import $module" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $module installed" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $module missing" -ForegroundColor Red
            $missingModules += $module
        }
    } catch {
        Write-Host "  ✗ $module missing" -ForegroundColor Red
        $missingModules += $module
    }
}

if ($missingModules.Count -gt 0) {
    Write-Host ""
    Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
}

# Check if database exists
Write-Host ""
Write-Host "Checking database..." -ForegroundColor Yellow

$dbPath = "src\charity_pos.db"

if (Test-Path $dbPath) {
    Write-Host "  ✓ Database found: $dbPath" -ForegroundColor Green
} else {
    Write-Host "  ℹ Database not found. Creating new database..." -ForegroundColor Yellow
    Set-Location src
    python init_database.py
    Set-Location ..
    
    if (Test-Path $dbPath) {
        Write-Host "  ✓ Database created successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to create database" -ForegroundColor Red
        exit 1
    }
}

# Display login credentials
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Default Login Credentials:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Admin:     username='admin'     password='admin123'" -ForegroundColor White
Write-Host "  Volunteer: username='volunteer' password='volunteer123'" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT: Change default passwords in production!" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Launch application
Write-Host "Launching Charity Shop POS System..." -ForegroundColor Green
Write-Host ""

Set-Location src
python main.py

# Cleanup on exit
Set-Location ..
Write-Host ""
Write-Host "Application closed. Thank you for using Charity POS!" -ForegroundColor Cyan



