# Charity Shop POS - Quick Start Guide

## Launch the Application

### Option 1: PowerShell (Recommended)

```powershell
cd C:\Users\Fab2\Desktop\AI\Specs\SPECs\Testing\TGCAATGC\spec_charity_pos
.\launch.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Option 2: Batch File (Simple)

Double-click: `launch.bat`

Or from command prompt:
```cmd
cd C:\Users\Fab2\Desktop\AI\Specs\SPECs\Testing\TGCAATGC\spec_charity_pos
launch.bat
```

### Option 3: Manual Launch

```powershell
cd C:\Users\Fab2\Desktop\AI\Specs\SPECs\Testing\TGCAATGC\spec_charity_pos\src
python main.py
```

---

## What the Launch Script Does

1. ✓ Checks Python installation
2. ✓ Checks/installs dependencies (SQLAlchemy, Flask, pytest)
3. ✓ Creates database if it doesn't exist
4. ✓ Initializes with sample data
5. ✓ Launches the application

---

## Test the System

Run all component tests:

```powershell
.\test_launch.ps1
```

This tests:
- Shopping Cart
- Payment Processing
- Receipt Generation
- Authentication
- Database Operations

---

## Login Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Volunteer:**
- Username: `volunteer`
- Password: `volunteer123`

⚠️ **Change these passwords before production use!**

---

## Quick Test Workflow

1. **Run the launcher:**
   ```powershell
   .\launch.ps1
   ```

2. **Login as volunteer**

3. **Process a test sale:**
   - Select "1. Process Sale"
   - Select "1. Add item to cart"
   - Search for "book"
   - Select item #1
   - Enter quantity: 1
   - Select "3. Complete sale"
   - Choose "1. Cash"
   - Enter cash: 10.00
   - Receipt generated!

4. **Check the receipt:**
   - Look in `src/receipts/` folder
   - Open the HTML file in your browser

---

## Troubleshooting

### "Python not found"
Install Python 3.8+ from python.org

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Database not found"
```powershell
cd src
python init_database.py
```

### "Can't run PowerShell scripts"
Either:
- Use `launch.bat` instead
- Or enable scripts: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## File Locations

- **Database:** `src/charity_pos.db`
- **Receipts:** `src/receipts/`
- **Reports:** `src/reports/`
- **Backups:** `src/backups/`

---

## Next Steps

- Change default passwords (edit `init_database.py`)
- Configure payment processor (edit `payment_processor.py`)
- Customize shop details (edit `receipt_generator.py`)
- Add more inventory items through the app

---

**Need help?** Check `README.md` for full documentation.



