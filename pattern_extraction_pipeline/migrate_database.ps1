# Neo4j Database Migration PowerShell Script
# Wrapper for the Python migration script with automatic .env update

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Neo4j Database Migration: 'neo4j' -> 'specengine'" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file from env.template first." -ForegroundColor Yellow
    exit 1
}

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    exit 1
}

# Check if neo4j package is installed
Write-Host "[CHECK] Verifying neo4j Python package..." -ForegroundColor Yellow
$neo4jInstalled = python -c "import neo4j; print('OK')" 2>$null
if ($neo4jInstalled -ne "OK") {
    Write-Host "[ERROR] neo4j Python package not installed!" -ForegroundColor Red
    Write-Host "[ACTION] Installing neo4j package..." -ForegroundColor Yellow
    pip install neo4j
}

# Ask which migration to run
Write-Host "[QUESTION] Migration type:" -ForegroundColor Yellow
Write-Host "  1. Selective migration (recommended) - moves ONLY pattern extraction data" -ForegroundColor Green
Write-Host "  2. Full migration - moves ALL data from source to target" -ForegroundColor Gray
Write-Host ""
$choice = Read-Host "Choose migration type (1 or 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "[ACTION] Running selective migration script..." -ForegroundColor Yellow
    Write-Host ""
    python migrate_database_selective.py
} else {
    Write-Host ""
    Write-Host "[ACTION] Running full migration script..." -ForegroundColor Yellow
    Write-Host ""
    python migrate_database.py
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Migration failed!" -ForegroundColor Red
    exit 1
}

# Ask if user wants to update .env file
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Update Configuration File" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Do you want to update .env file now?" -ForegroundColor Yellow
Write-Host "  Change: NEO4J_DATABASE=patterns" -ForegroundColor Gray
Write-Host "  To:     NEO4J_DATABASE=specengine" -ForegroundColor Green
Write-Host ""
$response = Read-Host "Update .env file? (yes/no)"

if ($response -eq "yes") {
    # Backup current .env
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    Copy-Item .env ".env.backup.$timestamp"
    Write-Host "[OK] Backed up .env to .env.backup.$timestamp" -ForegroundColor Green
    
    # Update .env file
    $content = Get-Content .env
    $updatedContent = $content -replace "NEO4J_DATABASE=patterns", "NEO4J_DATABASE=specengine"
    $updatedContent | Set-Content .env
    
    Write-Host "[OK] Updated .env file successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Current configuration:" -ForegroundColor Cyan
    Get-Content .env | Select-String "NEO4J"
} else {
    Write-Host "[SKIP] .env file not updated. Please update it manually:" -ForegroundColor Yellow
    Write-Host "  NEO4J_DATABASE=specengine" -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Migration Process Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Important reminders:" -ForegroundColor Yellow
Write-Host "  1. Restart any services that use the database" -ForegroundColor Gray
Write-Host "  2. Test your application with the new 'specengine' database" -ForegroundColor Gray
Write-Host "  3. The 'patterns' database has been cleaned" -ForegroundColor Gray
Write-Host ""
