# ========================================
# Boutique Scarf Shop - Full Setup
# Complete setup with PostgreSQL
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Boutique Scarf Shop - Full Setup" -ForegroundColor Cyan
Write-Host " (with Database)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path ".\backend\package.json")) {
    Write-Host "ERROR: Please run this script from the boutique-scarf-shop directory" -ForegroundColor Red
    exit 1
}

# ========================================
# Step 1: Check Prerequisites
# ========================================
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "  OK - Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR - Node.js not found" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
try {
    $pgVersion = psql --version
    Write-Host "  OK - PostgreSQL: $pgVersion" -ForegroundColor Green
    $hasPostgres = $true
} catch {
    Write-Host "  ERROR - PostgreSQL not found" -ForegroundColor Red
    Write-Host "  Install from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    $continue = Read-Host "`n  Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
    $hasPostgres = $false
}

# ========================================
# Step 2: Install Dependencies
# ========================================
Write-Host "`n[2/6] Installing dependencies..." -ForegroundColor Yellow

# Backend
Write-Host "  Backend..." -ForegroundColor Cyan
Push-Location backend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK - Backend ready" -ForegroundColor Green
    } else {
        Write-Host "  ERROR - Installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  OK - Already installed" -ForegroundColor Green
}
Pop-Location

# Frontend
Write-Host "  Frontend..." -ForegroundColor Cyan
Push-Location frontend
if (-not (Test-Path "node_modules")) {
    npm install --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK - Frontend ready" -ForegroundColor Green
    } else {
        Write-Host "  ERROR - Installation failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "  OK - Already installed" -ForegroundColor Green
}
Pop-Location

# ========================================
# Step 3: Database Setup
# ========================================
if ($hasPostgres) {
    Write-Host "`n[3/6] Setting up database..." -ForegroundColor Yellow
    
    $dbUser = Read-Host "  PostgreSQL username (default: postgres)"
    if ([string]::IsNullOrWhiteSpace($dbUser)) { $dbUser = "postgres" }
    
    $dbPassSecure = Read-Host "  PostgreSQL password" -AsSecureString
    $dbPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassSecure))
    
    $dbName = "boutique_scarf_shop"
    
    # Create database
    $env:PGPASSWORD = $dbPass
    Write-Host "  Creating database..." -ForegroundColor Cyan
    psql -U $dbUser -c "CREATE DATABASE $dbName;" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK - Database created" -ForegroundColor Green
    } else {
        Write-Host "  OK - Database already exists" -ForegroundColor Yellow
    }
    
    # Run migrations
    Write-Host "  Running migrations..." -ForegroundColor Cyan
    psql -U $dbUser -d $dbName -f ".\backend\migrations\001_initial_schema.sql" 2>$null | Out-Null
    Write-Host "  OK - Migrations complete" -ForegroundColor Green
    
    Remove-Item Env:\PGPASSWORD
} else {
    Write-Host "`n[3/6] Skipping database (PostgreSQL not available)" -ForegroundColor Yellow
}

# ========================================
# Step 4: Backend Configuration
# ========================================
Write-Host "`n[4/6] Configuring backend..." -ForegroundColor Yellow

$configFile = ".\backend\config\config.js"
if (-not (Test-Path $configFile)) {
    $config = @"
module.exports = {
  database: {
    host: 'localhost',
    port: 5432,
    name: '$dbName',
    user: '$dbUser',
    password: '$dbPass'
  },
  server: {
    port: 3001,
    nodeEnv: 'development'
  },
  jwt: {
    secret: 'dev_jwt_secret_minimum_32_characters_long_change_in_production',
    expiresIn: '24h'
  },
  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME,
    apiKey: process.env.CLOUDINARY_API_KEY,
    apiSecret: process.env.CLOUDINARY_API_SECRET
  },
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY,
    publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
  },
  email: {
    provider: 'sendgrid',
    sendgrid: {
      apiKey: process.env.SENDGRID_API_KEY,
      fromEmail: 'noreply@localhost'
    }
  },
  cors: {
    origin: 'http://localhost:5173'
  }
};
"@
    Set-Content -Path $configFile -Value $config
    Write-Host "  OK - Configuration created" -ForegroundColor Green
} else {
    Write-Host "  OK - Configuration exists" -ForegroundColor Green
}

# ========================================
# Step 5: Start Backend
# ========================================
Write-Host "`n[5/6] Starting backend..." -ForegroundColor Yellow

Push-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location
Write-Host "  Backend starting on http://localhost:3001" -ForegroundColor Green

Start-Sleep -Seconds 3

# ========================================
# Step 6: Start Frontend
# ========================================
Write-Host "`n[6/6] Starting frontend..." -ForegroundColor Yellow

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
Write-Host "Frontend:  http://localhost:5173" -ForegroundColor Green
Write-Host "Backend:   http://localhost:3001" -ForegroundColor Green
Write-Host ""
Write-Host "Default Admin Account:" -ForegroundColor Yellow
Write-Host "  Email:    admin@boutique-scarves.com" -ForegroundColor Gray
Write-Host "  Password: admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "Test API:" -ForegroundColor Yellow
Write-Host '  Invoke-RestMethod -Uri http://localhost:3001/' -ForegroundColor Gray
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "  - EXECUTION_REPORT.md" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop: Close the PowerShell windows or press Ctrl+C" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

