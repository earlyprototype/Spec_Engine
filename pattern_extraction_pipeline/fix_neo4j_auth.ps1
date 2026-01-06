# Fix Neo4j Authentication
# The new container needs the password to be properly set

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Neo4j Authentication Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[INFO] Neo4j Browser URL: http://localhost:7475" -ForegroundColor Yellow
Write-Host ""
Write-Host "Please follow these steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open http://localhost:7475 in your browser" -ForegroundColor White
Write-Host "2. Connect with:" -ForegroundColor White
Write-Host "   - URI: bolt://localhost:7688" -ForegroundColor Gray
Write-Host "   - Username: neo4j" -ForegroundColor Gray
Write-Host "   - Password: specengine123" -ForegroundColor Gray
Write-Host ""
Write-Host "3. If prompted to change password, set it to: specengine123" -ForegroundColor White
Write-Host ""
Write-Host "4. Then run this command to verify:" -ForegroundColor White
Write-Host "   python quick_test.py" -ForegroundColor Cyan
Write-Host ""

# Try to open browser
Write-Host "Opening Neo4j Browser..." -ForegroundColor Yellow
Start-Process "http://localhost:7475"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Waiting for you to complete authentication in browser..." -ForegroundColor Yellow
Write-Host "Press Enter when done" -ForegroundColor Yellow
Read-Host

# Test connection
Write-Host ""
Write-Host "[TEST] Testing connection..." -ForegroundColor Yellow
python quick_test.py
