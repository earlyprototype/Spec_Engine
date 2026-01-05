# setup.ps1
# Windows PowerShell setup script for Pattern Extraction Pipeline

Write-Host "=== Pattern Extraction Pipeline Setup ===" -ForegroundColor Green

# Check if Docker is installed
Write-Host "`nChecking Docker installation..." -ForegroundColor Yellow
try {
    docker --version
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Python is installed
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
try {
    python --version
    Write-Host "✓ Python is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Start Neo4j container
Write-Host "`nStarting Neo4j container..." -ForegroundColor Yellow
docker run -d `
    --name spec-engine-graph `
    -p 7474:7474 -p 7687:7687 `
    -e NEO4J_AUTH=neo4j/password `
    neo4j

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Neo4j container started" -ForegroundColor Green
    Write-Host "  Browser UI: http://localhost:7474" -ForegroundColor Cyan
    Write-Host "  Username: neo4j" -ForegroundColor Cyan
    Write-Host "  Password: password" -ForegroundColor Cyan
} else {
    Write-Host "⚠ Neo4j container may already exist or Docker is not running" -ForegroundColor Yellow
    Write-Host "  Try: docker start spec-engine-graph" -ForegroundColor Cyan
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check if .env exists
Write-Host "`nChecking environment configuration..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠ .env file not found" -ForegroundColor Yellow
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item env.template .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "" -ForegroundColor Yellow
    Write-Host "IMPORTANT: Edit .env and add your credentials:" -ForegroundColor Red
    Write-Host "  - GITHUB_TOKEN (get from: https://github.com/settings/tokens)" -ForegroundColor Yellow
    Write-Host "  - OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)" -ForegroundColor Yellow
}

# Wait for Neo4j to be ready
Write-Host "`nWaiting for Neo4j to be ready (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host "✓ Neo4j should be ready now" -ForegroundColor Green

# Final instructions
Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your API keys" -ForegroundColor White
Write-Host "2. Run: python test_extraction.py (test single repo extraction)" -ForegroundColor White
Write-Host "3. Run: python test_query.py (test graph queries)" -ForegroundColor White
Write-Host "4. Run: python pattern_extractor.py (extract 20 patterns)" -ForegroundColor White
Write-Host "`nTo stop Neo4j: docker stop spec-engine-graph" -ForegroundColor Yellow
Write-Host "To start Neo4j: docker start spec-engine-graph" -ForegroundColor Yellow
