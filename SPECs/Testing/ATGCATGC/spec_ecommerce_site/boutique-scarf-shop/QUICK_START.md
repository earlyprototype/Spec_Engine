# Quick Start Guide

## Which Script Should I Use?

### Option 1: Full Experience (Recommended)
```powershell
.\start-with-database.ps1
```

**Use this if you want:**
- ✓ Complete working application
- ✓ User registration and login
- ✓ Product management
- ✓ Shopping cart functionality
- ✓ Full API testing
- ✓ Production-like environment

**Requirements:**
- Node.js 18+
- PostgreSQL 14+

**What happens:**
1. Checks prerequisites
2. Installs dependencies (backend + frontend)
3. Creates database
4. Runs migrations
5. Creates configuration
6. Starts both servers
7. Opens browser

**Time:** ~5-10 minutes (first run)

---

### Option 2: Quick Preview (No Database)
```powershell
.\start-without-database.ps1
```

**Use this if you want:**
- ✓ Quick server test
- ✓ See frontend design
- ✓ Test API structure
- ✓ No database setup required

**Limitations:**
- ✗ No user authentication
- ✗ No product data
- ✗ Database operations will fail

**Requirements:**
- Node.js 18+ only

**What happens:**
1. Checks Node.js
2. Installs dependencies
3. Creates minimal config
4. Starts servers
5. Opens browser

**Time:** ~2-3 minutes

---

## Troubleshooting

### Scripts won't run
```powershell
# Enable PowerShell scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PostgreSQL not installed
- Download: https://www.postgresql.org/download/windows/
- Or use Docker: 
  ```powershell
  docker run --name postgres-boutique -e POSTGRES_PASSWORD=yourpass -p 5432:5432 -d postgres:16
  ```

### Node.js not installed
- Download: https://nodejs.org (LTS version recommended)

---

## What You'll See

### Frontend (http://localhost:5173)
- Beautiful landing page
- Feature cards
- Product grid
- API documentation
- Development status dashboard

### Backend (http://localhost:3001)
- API health check
- RESTful endpoints
- JWT authentication
- Stripe integration ready
- Cloudinary integration ready

---

## After Starting

### Default Admin Account
(Only with database setup)
- **Email:** admin@boutique-scarves.com
- **Password:** admin123

### Test the API

**Health Check:**
```powershell
Invoke-RestMethod -Uri http://localhost:3001/
```

**Register User:**
```powershell
$body = @{
    email = "test@example.com"
    password = "Test123456"
    firstName = "Test"
    lastName = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:3001/api/auth/register -Method Post -Body $body -ContentType "application/json"
```

**Login:**
```powershell
$body = @{
    email = "test@example.com"
    password = "Test123456"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:3001/api/auth/login -Method Post -Body $body -ContentType "application/json"
$token = $response.token
```

**Get Products:**
```powershell
Invoke-RestMethod -Uri http://localhost:3001/api/products
```

**Get Cart (requires token):**
```powershell
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri http://localhost:3001/api/cart -Headers $headers
```

---

## Stopping the Servers

1. Close the PowerShell windows that opened, or
2. Press `Ctrl+C` in each server terminal

---

## Next Steps

1. **Add Products** (as admin via API)
2. **Configure Stripe** (for payments)
3. **Configure Cloudinary** (for images)
4. **Set up SendGrid** (for emails)
5. **Build Frontend UI** (React components)

See `SETUP_GUIDE.md` for detailed instructions.

---

## Decision Tree

```
Do you have PostgreSQL installed?
│
├─ Yes ──→ Use: start-with-database.ps1
│          Get: Full functionality
│          Time: 5-10 minutes
│
└─ No ───→ Do you want to install it?
           │
           ├─ Yes ──→ Install PostgreSQL
           │          Then use: start-with-database.ps1
           │
           └─ No ───→ Use: start-without-database.ps1
                      Get: Preview only
                      Time: 2-3 minutes
```

---

## Getting Help

- **Detailed Setup:** See `SETUP_GUIDE.md`
- **Full Documentation:** See `EXECUTION_REPORT.md`
- **API Reference:** See `SETUP_GUIDE.md` (API Endpoints section)
- **Tech Stack:** See `docs/TECH_STACK.md`
- **Database:** See `docs/DATABASE_SCHEMA.md`

---

## System Requirements

### Minimum
- Windows 10/11
- Node.js 18+
- 2 GB RAM
- 1 GB disk space

### Recommended
- Windows 11
- Node.js 20+
- PostgreSQL 16+
- 4 GB RAM
- 2 GB disk space

---

**Ready to start?**

```powershell
# Full version
.\start-with-database.ps1

# Quick preview
.\start-without-database.ps1
```

