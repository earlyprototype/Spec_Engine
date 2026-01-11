# check_models.ps1
# Check available Gemini models

Write-Host "Checking available Gemini models..." -ForegroundColor Cyan
Write-Host ""

# Load .env and set environment variable
Get-Content .env | ForEach-Object {
    if ($_ -match '^GEMINI_API_KEY=(.+)$') {
        $env:GEMINI_API_KEY = $matches[1].Trim()
    }
}

# Run the Python script
python check_gemini_models.py

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
