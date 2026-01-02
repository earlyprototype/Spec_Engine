# ========================================
# Boutique Scarf Shop - Quick Start
# Simple launcher without database
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Boutique Scarf Shop - Quick Start" -ForegroundColor Cyan
Write-Host " (No Database Required)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path ".\backend\package.json")) {
    Write-Host "ERROR: Please run this script from the boutique-scarf-shop directory" -ForegroundColor Red
    exit 1
}

# ========================================
# Step 1: Check Node.js
# ========================================
Write-Host "[1/4] Checking Node.js..." -ForegroundColor Yellow

try {
    $nodeVersion = node --version
    Write-Host "  OK - Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR - Node.js not found. Install from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# ========================================
# Step 2: Install Dependencies
# ========================================
Write-Host "`n[2/4] Installing dependencies..." -ForegroundColor Yellow

# Backend
Write-Host "  Installing backend..." -ForegroundColor Cyan
Push-Location backend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK - Backend ready" -ForegroundColor Green
    } else {
        Write-Host "  ERROR - Backend installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  OK - Backend already installed" -ForegroundColor Green
}
Pop-Location

# Frontend
Write-Host "  Installing frontend..." -ForegroundColor Cyan
Push-Location frontend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK - Frontend ready" -ForegroundColor Green
    } else {
        Write-Host "  ERROR - Frontend installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  OK - Frontend already installed" -ForegroundColor Green
}
Pop-Location

# ========================================
# Step 3: Configure Backend
# ========================================
Write-Host "`n[3/4] Setting up configuration..." -ForegroundColor Yellow

$configFile = ".\backend\config\config.js"
if (-not (Test-Path $configFile)) {
    $config = @'
module.exports = {
  database: { host: 'localhost', port: 5432, name: 'boutique', user: 'postgres', password: 'postgres' },
  server: { port: 3001, nodeEnv: 'development' },
  jwt: { secret: 'dev_jwt_secret_minimum_32_characters_long_for_testing', expiresIn: '24h' },
  cloudinary: { cloudName: 'not_configured', apiKey: 'not_configured', apiSecret: 'not_configured' },
  stripe: { secretKey: 'sk_test_not_configured', publishableKey: 'pk_test_not_configured', webhookSecret: 'whsec_not_configured' },
  email: { provider: 'sendgrid', sendgrid: { apiKey: 'not_configured', fromEmail: 'noreply@localhost' } },
  cors: { origin: 'http://localhost:5173' }
};
'@
    Set-Content -Path $configFile -Value $config
    Write-Host "  OK - Configuration created" -ForegroundColor Green
} else {
    Write-Host "  OK - Configuration exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "  WARNING: Database operations will fail" -ForegroundColor Yellow
Write-Host "  This mode is for testing server setup only" -ForegroundColor Yellow

# ========================================
# Step 4: Start Servers
# ========================================
Write-Host "`n[4/4] Starting servers..." -ForegroundColor Yellow

# Backend
Push-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location
Write-Host "  Backend starting on http://localhost:3001" -ForegroundColor Green

Start-Sleep -Seconds 2

# Frontend
Push-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location
Write-Host "  Frontend starting on http://localhost:5173" -ForegroundColor Green

Start-Sleep -Seconds 3

# Open browser
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "Backend:  http://localhost:3001" -ForegroundColor Green
Write-Host ""
Write-Host "What works:" -ForegroundColor Yellow
Write-Host "  - Server starts" -ForegroundColor Gray
Write-Host "  - Frontend displays" -ForegroundColor Gray
Write-Host "  - Health check works" -ForegroundColor Gray
Write-Host ""
Write-Host "What does NOT work (no database):" -ForegroundColor Yellow
Write-Host "  - User registration/login" -ForegroundColor Gray
Write-Host "  - Product listing" -ForegroundColor Gray
Write-Host "  - Shopping cart" -ForegroundColor Gray
Write-Host "  - Orders" -ForegroundColor Gray
Write-Host ""
Write-Host "To enable full features, run: .\start-full.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

