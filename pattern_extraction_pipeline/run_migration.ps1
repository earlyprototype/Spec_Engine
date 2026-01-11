# Run Migration - Interactive wrapper
# This script handles the current directory properly

$originalLocation = Get-Location

try {
    # Navigate to the script directory
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $scriptPath
    
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Pattern Extraction Database Migration" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This will:" -ForegroundColor Yellow
    Write-Host "  - Move pattern extraction data to 'specengine' database" -ForegroundColor Gray
    Write-Host "  - Leave other project data in 'neo4j' database" -ForegroundColor Gray
    Write-Host "  - Update your .env file" -ForegroundColor Gray
    Write-Host ""
    
    # Run the Python script
    python migrate_database_selective.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Cyan
        Write-Host "Update Configuration" -ForegroundColor Cyan
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
            $updatedContent = $content -replace "NEO4J_DATABASE=.*", "NEO4J_DATABASE=specengine"
            $updatedContent | Set-Content .env
            
            Write-Host "[OK] Updated .env file successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Current Neo4j configuration:" -ForegroundColor Cyan
            Get-Content .env | Select-String "NEO4J"
        } else {
            Write-Host "[SKIP] .env file not updated. Please update it manually:" -ForegroundColor Yellow
            Write-Host "  NEO4J_DATABASE=specengine" -ForegroundColor Gray
        }
        
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "Migration Complete!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[ERROR] Migration failed. Check errors above." -ForegroundColor Red
    }
}
finally {
    Set-Location $originalLocation
}
