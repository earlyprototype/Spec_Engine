# Setup New Neo4j Container for Spec Engine
# This script creates a dedicated Neo4j instance for the pattern extraction project

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Spec Engine Neo4j Container Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/5] Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "[ERROR] Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Docker is running" -ForegroundColor Green

# Check if container already exists
Write-Host ""
Write-Host "[2/5] Checking for existing container..." -ForegroundColor Yellow
$existingContainer = docker ps -a --filter "name=spec-engine-neo4j" --format "{{.Names}}"
if ($existingContainer) {
    Write-Host "[WARNING] Container 'spec-engine-neo4j' already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove it and recreate? (yes/no)"
    if ($response -eq "yes") {
        Write-Host "[ACTION] Stopping and removing existing container..." -ForegroundColor Yellow
        docker stop spec-engine-neo4j 2>$null
        docker rm spec-engine-neo4j 2>$null
        Write-Host "[OK] Removed existing container" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] Keeping existing container" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "If the container is stopped, you can start it with:" -ForegroundColor Cyan
        Write-Host "  docker start spec-engine-neo4j" -ForegroundColor White
        exit 0
    }
}

# Check if ports are available
Write-Host ""
Write-Host "[3/5] Checking port availability..." -ForegroundColor Yellow
$port7688 = Get-NetTCPConnection -LocalPort 7688 -ErrorAction SilentlyContinue
$port7475 = Get-NetTCPConnection -LocalPort 7475 -ErrorAction SilentlyContinue

if ($port7688) {
    Write-Host "[WARNING] Port 7688 is already in use" -ForegroundColor Yellow
    Write-Host "The new Neo4j Bolt port may conflict" -ForegroundColor Yellow
}
if ($port7475) {
    Write-Host "[WARNING] Port 7475 is already in use" -ForegroundColor Yellow
    Write-Host "The new Neo4j HTTP port may conflict" -ForegroundColor Yellow
}

if (-not $port7688 -and -not $port7475) {
    Write-Host "[OK] Ports 7688 and 7475 are available" -ForegroundColor Green
}

# Start the new container
Write-Host ""
Write-Host "[4/5] Starting new Neo4j container..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Container started successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to start container" -ForegroundColor Red
    exit 1
}

# Wait for Neo4j to be ready
Write-Host ""
Write-Host "[5/5] Waiting for Neo4j to be ready..." -ForegroundColor Yellow
Write-Host "This may take 30-60 seconds..." -ForegroundColor Gray

$maxAttempts = 60
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    $attempt++
    Start-Sleep -Seconds 2
    
    # Check health status
    $health = docker inspect --format='{{.State.Health.Status}}' spec-engine-neo4j 2>$null
    
    if ($health -eq "healthy") {
        $ready = $true
        Write-Host "[OK] Neo4j is ready!" -ForegroundColor Green
    } else {
        Write-Host "  Attempt $attempt/$maxAttempts - Status: $health" -ForegroundColor Gray
    }
}

if (-not $ready) {
    Write-Host "[WARNING] Neo4j health check timeout" -ForegroundColor Yellow
    Write-Host "The container may still be starting up. Check with:" -ForegroundColor Yellow
    Write-Host "  docker logs spec-engine-neo4j" -ForegroundColor White
}

# Display connection info
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Container Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Connection Details:" -ForegroundColor Yellow
Write-Host "  Browser UI:   http://localhost:7475" -ForegroundColor White
Write-Host "  Bolt URI:     bolt://localhost:7688" -ForegroundColor White
Write-Host "  Username:     neo4j" -ForegroundColor White
Write-Host "  Password:     specengine123" -ForegroundColor White
Write-Host ""
Write-Host "Container Name: spec-engine-neo4j" -ForegroundColor Gray
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Update your .env file (automatic backup will be created)" -ForegroundColor White
Write-Host "  2. Run migration: .\migrate_to_new_container.ps1" -ForegroundColor White
Write-Host "  3. Verify in browser: http://localhost:7475" -ForegroundColor White
Write-Host ""

# Ask if user wants to update .env now
Write-Host "============================================================" -ForegroundColor Cyan
$response = Read-Host "Do you want to update .env file now? (yes/no)"

if ($response -eq "yes") {
    # Backup current .env
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    Copy-Item .env ".env.backup.$timestamp"
    Write-Host "[OK] Backed up .env to .env.backup.$timestamp" -ForegroundColor Green
    
    # Update .env file
    $content = Get-Content .env
    $updatedContent = $content -replace "NEO4J_URI=.*", "NEO4J_URI=bolt://localhost:7688"
    $updatedContent = $updatedContent -replace "NEO4J_PASSWORD=.*", "NEO4J_PASSWORD=specengine123"
    $updatedContent = $updatedContent -replace "NEO4J_DATABASE=.*", "NEO4J_DATABASE=neo4j"
    $updatedContent | Set-Content .env
    
    Write-Host "[OK] Updated .env file!" -ForegroundColor Green
    Write-Host ""
    Write-Host "New configuration:" -ForegroundColor Cyan
    Get-Content .env | Select-String "NEO4J"
    Write-Host ""
    Write-Host "Note: Community Edition only supports one database (neo4j)" -ForegroundColor Gray
    Write-Host "      Database separation is achieved via separate containers" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "[SKIP] .env not updated. Update manually with:" -ForegroundColor Yellow
    Write-Host "  NEO4J_URI=bolt://localhost:7688" -ForegroundColor White
    Write-Host "  NEO4J_PASSWORD=specengine123" -ForegroundColor White
    Write-Host "  NEO4J_DATABASE=neo4j" -ForegroundColor White
}

Write-Host ""
Write-Host "To view logs:    docker logs spec-engine-neo4j" -ForegroundColor Gray
Write-Host "To stop:         docker stop spec-engine-neo4j" -ForegroundColor Gray
Write-Host "To start:        docker start spec-engine-neo4j" -ForegroundColor Gray
Write-Host "To remove:       docker-compose down" -ForegroundColor Gray
Write-Host ""
