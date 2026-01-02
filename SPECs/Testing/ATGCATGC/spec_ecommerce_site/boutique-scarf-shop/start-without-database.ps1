# ========================================
# Boutique Scarf Shop - Start without Database
# Quick API testing setup (mock mode)
# ========================================

Write-Host @"
╔════════════════════════════════════════════════╗
║   Boutique Handcrafted Scarf Shop              ║
║   Quick Start (without Database)               ║
║   API Testing Mode                             ║
╚════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if running from correct directory
if (-not (Test-Path ".\backend\package.json")) {
    Write-Host "Error: Please run this script from the boutique-scarf-shop directory" -ForegroundColor Red
    exit 1
}

# ========================================
# Step 1: Check Prerequisites
# ========================================
Write-Host "`n[1/5] Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found. Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "  ✓ npm installed: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm not found" -ForegroundColor Red
    exit 1
}

Write-Host "  ℹ PostgreSQL: Skipped (not required for API testing)" -ForegroundColor Gray

# ========================================
# Step 2: Install Dependencies
# ========================================
Write-Host "`n[2/5] Installing dependencies..." -ForegroundColor Yellow

# Backend
Write-Host "  Installing backend dependencies..." -ForegroundColor Cyan
Push-Location backend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Backend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Backend installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  ✓ Backend dependencies already installed" -ForegroundColor Green
}
Pop-Location

# Frontend
Write-Host "  Installing frontend dependencies..." -ForegroundColor Cyan
Push-Location frontend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Frontend installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  ✓ Frontend dependencies already installed" -ForegroundColor Green
}
Pop-Location

# ========================================
# Step 3: Backend Configuration (Mock Mode)
# ========================================
Write-Host "`n[3/5] Configuring backend (mock mode)..." -ForegroundColor Yellow

$configFile = ".\backend\config\config.js"
if (-not (Test-Path $configFile)) {
    Write-Host "  Creating minimal config.js..." -ForegroundColor Cyan
    
    $config = @"
// Minimal configuration for API testing (no database)
module.exports = {
  database: {
    host: 'localhost',
    port: 5432,
    name: 'boutique_scarf_shop',
    user: 'postgres',
    password: 'postgres'
  },
  server: {
    port: 3001,
    nodeEnv: 'development'
  },
  jwt: {
    secret: 'dev_jwt_secret_minimum_32_characters_long_for_testing',
    expiresIn: '24h'
  },
  cloudinary: {
    cloudName: 'not_configured',
    apiKey: 'not_configured',
    apiSecret: 'not_configured'
  },
  stripe: {
    secretKey: 'sk_test_not_configured',
    publishableKey: 'pk_test_not_configured',
    webhookSecret: 'whsec_not_configured'
  },
  email: {
    provider: 'sendgrid',
    sendgrid: {
      apiKey: 'not_configured',
      fromEmail: 'noreply@localhost'
    }
  },
  cors: {
    origin: 'http://localhost:5173'
  }
};
"@
    
    Set-Content -Path $configFile -Value $config
    Write-Host "  ✓ Minimal configuration created" -ForegroundColor Green
} else {
    Write-Host "  ✓ Configuration already exists" -ForegroundColor Green
}

Write-Host "
  ⚠ WARNING: Database operations will fail" -ForegroundColor Yellow
Write-Host "    This mode is for testing API endpoints that don't need DB" -ForegroundColor Yellow
Write-Host "    Server health check will work: GET http://localhost:3001/" -ForegroundColor Yellow

# ========================================
# Step 4: Start Servers
# ========================================
Write-Host "`n[4/5] Starting servers..." -ForegroundColor Yellow

# Backend
Write-Host "  Starting backend server..." -ForegroundColor Cyan
Push-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location
Write-Host "  ✓ Backend server starting on http://localhost:3001" -ForegroundColor Green
Start-Sleep -Seconds 3

# Frontend
Write-Host "  Starting frontend server..." -ForegroundColor Cyan
Push-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location
Write-Host "  ✓ Frontend server starting on http://localhost:5173" -ForegroundColor Green
Start-Sleep -Seconds 3

# ========================================
# Step 5: Open Browser & Show Info
# ========================================
Write-Host "`n[5/5] Opening browser..." -ForegroundColor Yellow

Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host @"
╔════════════════════════════════════════════════╗
║   Quick Start Complete! 🚀                    ║
║   (API Testing Mode - No Database)            ║
╚════════════════════════════════════════════════╝

Frontend:  http://localhost:5173
Backend:   http://localhost:3001

✓ Working Endpoints (No DB Required):
  GET  http://localhost:3001/          (Health check)
  
✗ Limited Endpoints (Need Database):
  POST /api/auth/register               (Will fail without DB)
  POST /api/auth/login                  (Will fail without DB)
  GET  /api/products                    (Will fail without DB)
  All other endpoints require database

Test the API:
  # Health check (works without DB)
  Invoke-RestMethod -Uri http://localhost:3001/

What Works:
  ✓ Server starts and responds
  ✓ Frontend loads and displays
  ✓ API structure is accessible
  ✓ CORS is configured
  ✓ Endpoint routing works

What Does NOT Work (Without DB):
  ✗ User registration/login
  ✗ Product listing
  ✗ Shopping cart
  ✗ Orders
  ✗ All database operations

Next Steps:
  To enable full functionality:
  1. Install PostgreSQL
  2. Run: .\start-with-database.ps1

Or continue testing API structure and server setup!

To stop servers:
  Close the PowerShell windows or press Ctrl+C in each

Documentation:
  - SETUP_GUIDE.md      - Complete setup instructions
  - EXECUTION_REPORT.md - Full project documentation

Press any key to exit this window...
"@ -ForegroundColor Cyan

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

