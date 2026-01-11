# Quick Setup Script for Pattern Extraction Pipeline
# Run this in PowerShell: .\QUICK_SETUP.ps1

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "PATTERN EXTRACTION PIPELINE - QUICK SETUP" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Install Python dependencies
Write-Host "[1/3] Installing Python packages..." -ForegroundColor Yellow
Write-Host "This may take a few minutes (building Neo4j driver from source)..." -ForegroundColor Gray
python -m pip install --quiet PyGithub google-generativeai neo4j python-dotenv

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] All packages installed" -ForegroundColor Green
} else {
    Write-Host "  [X] Package installation failed" -ForegroundColor Red
    exit 1
}

# 2. Check Neo4j
Write-Host ""
Write-Host "[2/3] Checking Neo4j..." -ForegroundColor Yellow
$neo4j = docker ps --filter "name=neo4j" --format "{{.Names}}"
if ($neo4j) {
    Write-Host "  [OK] Found Neo4j container: $neo4j" -ForegroundColor Green
} else {
    Write-Host "  [X] No Neo4j container running" -ForegroundColor Red
    Write-Host "  Start your existing Neo4j container" -ForegroundColor Yellow
}

# 3. Add database line to .env if not present
Write-Host ""
Write-Host "[3/3] Configuring database..." -ForegroundColor Yellow
$envContent = Get-Content .env -Raw
if ($envContent -notmatch "NEO4J_DATABASE") {
    Add-Content .env "`nNEO4J_DATABASE=specengine"
    Write-Host "  [OK] Added NEO4J_DATABASE=specengine to .env" -ForegroundColor Green
} else {
    Write-Host "  [OK] NEO4J_DATABASE already configured" -ForegroundColor Green
}

# Run readiness check
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Running full readiness check..." -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
python check_readiness.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! You're ready to extract patterns!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Try it now:" -ForegroundColor Cyan
    Write-Host "  python test_extraction.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Setup incomplete - check errors above" -ForegroundColor Red
}
