# ========================================
# Boutique Scarf Shop - Start with Database
# Complete setup including PostgreSQL
# ========================================

Write-Host @"
╔════════════════════════════════════════════════╗
║   Boutique Handcrafted Scarf Shop              ║
║   Full Setup (with Database)                   ║
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
Write-Host "`n[1/7] Checking prerequisites..." -ForegroundColor Yellow

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

# Check PostgreSQL
try {
    $pgVersion = psql --version
    Write-Host "  ✓ PostgreSQL installed: $pgVersion" -ForegroundColor Green
    $hasPostgres = $true
} catch {
    Write-Host "  ✗ PostgreSQL not found" -ForegroundColor Yellow
    Write-Host "    Install from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    $hasPostgres = $false
    
    $continue = Read-Host "`n  Continue without database setup? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# ========================================
# Step 2: Install Dependencies
# ========================================
Write-Host "`n[2/7] Installing dependencies..." -ForegroundColor Yellow

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
# Step 3: Database Configuration
# ========================================
if ($hasPostgres) {
    Write-Host "`n[3/7] Configuring database..." -ForegroundColor Yellow
    
    # Prompt for database credentials
    Write-Host "  Database setup:" -ForegroundColor Cyan
    $dbUser = Read-Host "  PostgreSQL username (default: postgres)"
    if ([string]::IsNullOrWhiteSpace($dbUser)) { $dbUser = "postgres" }
    
    $dbPass = Read-Host "  PostgreSQL password" -AsSecureString
    $dbPassPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPass))
    
    $dbName = "boutique_scarf_shop"
    
    # Check if database exists
    $env:PGPASSWORD = $dbPassPlain
    $dbExists = psql -U $dbUser -lqt 2>$null | Select-String -Pattern $dbName -Quiet
    
    if (-not $dbExists) {
        Write-Host "  Creating database: $dbName..." -ForegroundColor Cyan
        psql -U $dbUser -c "CREATE DATABASE $dbName;" 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Database created" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed to create database" -ForegroundColor Red
            Write-Host "    You may need to create it manually: CREATE DATABASE $dbName;" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ✓ Database already exists" -ForegroundColor Green
    }
    
    # Run migrations
    Write-Host "  Running migrations..." -ForegroundColor Cyan
    $migrationFile = ".\backend\migrations\001_initial_schema.sql"
    
    if (Test-Path $migrationFile) {
        psql -U $dbUser -d $dbName -f $migrationFile 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Migrations complete" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Migrations may have already run (this is OK)" -ForegroundColor Yellow
        }
    }
    
    Remove-Item Env:\PGPASSWORD
} else {
    Write-Host "`n[3/7] Skipping database setup (PostgreSQL not available)" -ForegroundColor Yellow
}

# ========================================
# Step 4: Backend Configuration
# ========================================
Write-Host "`n[4/7] Configuring backend..." -ForegroundColor Yellow

$configFile = ".\backend\config\config.js"
if (-not (Test-Path $configFile)) {
    Write-Host "  Creating config.js from template..." -ForegroundColor Cyan
    
    $config = @"
module.exports = {
  database: {
    host: 'localhost',
    port: 5432,
    name: '$dbName',
    user: '$dbUser',
    password: '$dbPassPlain'
  },
  server: {
    port: 3001,
    nodeEnv: 'development'
  },
  jwt: {
    secret: 'dev_jwt_secret_min_32_chars_change_in_production_abc123',
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
    Write-Host "  ✓ Configuration created" -ForegroundColor Green
    Write-Host "    Note: External services (Stripe, Cloudinary) need environment variables" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Configuration already exists" -ForegroundColor Green
}

# ========================================
# Step 5: Start Backend Server
# ========================================
Write-Host "`n[5/7] Starting backend server..." -ForegroundColor Yellow

Push-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location

Write-Host "  ✓ Backend server starting on http://localhost:3001" -ForegroundColor Green
Start-Sleep -Seconds 3

# ========================================
# Step 6: Start Frontend Server
# ========================================
Write-Host "`n[6/7] Starting frontend server..." -ForegroundColor Yellow

Push-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Pop-Location

Write-Host "  ✓ Frontend server starting on http://localhost:5173" -ForegroundColor Green
Start-Sleep -Seconds 3

# ========================================
# Step 7: Open Browser & Show Info
# ========================================
Write-Host "`n[7/7] Opening browser..." -ForegroundColor Yellow

Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host @"
╔════════════════════════════════════════════════╗
║   Setup Complete! 🚀                          ║
╚════════════════════════════════════════════════╝

Frontend:  http://localhost:5173
Backend:   http://localhost:3001

Default Admin Account:
  Email:    admin@boutique-scarves.com
  Password: admin123

Quick API Test (PowerShell):
  `$body = @{ email='test@example.com'; password='Test123456' } | ConvertTo-Json
  Invoke-RestMethod -Uri http://localhost:3001/api/auth/register -Method Post -Body `$body -ContentType 'application/json'

To stop servers:
  Close the PowerShell windows or press Ctrl+C in each

Documentation:
  - SETUP_GUIDE.md      - Complete setup guide
  - EXECUTION_REPORT.md - Full project documentation
  - docs/               - Technical documentation

Press any key to exit this window...
"@ -ForegroundColor Cyan

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

