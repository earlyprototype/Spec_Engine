# Charity Shop POS System - Test Script
# Runs all component tests to verify system is working

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Charity Shop POS System - Test Runner" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath\src

$testsPassed = 0
$testsFailed = 0

# Test 1: Shopping Cart
Write-Host "[TEST 1/5] Testing Shopping Cart..." -ForegroundColor Yellow
python cart.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Shopping Cart: PASSED" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "  ✗ Shopping Cart: FAILED" -ForegroundColor Red
    $testsFailed++
}

# Test 2: Payment Processing
Write-Host "[TEST 2/5] Testing Payment Processing..." -ForegroundColor Yellow
python payment_processor.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Payment Processing: PASSED" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "  ✗ Payment Processing: FAILED" -ForegroundColor Red
    $testsFailed++
}

# Test 3: Receipt Generation
Write-Host "[TEST 3/5] Testing Receipt Generation..." -ForegroundColor Yellow
python receipt_generator.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Receipt Generation: PASSED" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "  ✗ Receipt Generation: FAILED" -ForegroundColor Red
    $testsFailed++
}

# Test 4: Authentication
Write-Host "[TEST 4/5] Testing Authentication..." -ForegroundColor Yellow
python auth.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Authentication: PASSED" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "  ✗ Authentication: FAILED" -ForegroundColor Red
    $testsFailed++
}

# Test 5: Database Operations
Write-Host "[TEST 5/5] Testing Database..." -ForegroundColor Yellow
python database.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Database: PASSED" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "  ✗ Database: FAILED" -ForegroundColor Red
    $testsFailed++
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Test Results:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Passed: $testsPassed/5" -ForegroundColor Green
Write-Host "  Failed: $testsFailed/5" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "  ✓ All tests passed! System is ready." -ForegroundColor Green
} else {
    Write-Host "  ✗ Some tests failed. Check error messages above." -ForegroundColor Red
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location ..



