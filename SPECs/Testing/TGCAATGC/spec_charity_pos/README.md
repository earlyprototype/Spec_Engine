# Charity Shop Point of Sale System

A complete point of sale system for charity shops, featuring inventory management, sales processing, donation tracking, and reporting.

## Features

- **Inventory Management**
  - Add, edit, delete, and search items
  - Category management with hierarchical structure
  - Stock level tracking and low-stock alerts
  - Donation recording and tracking

- **Transaction Processing**
  - Shopping cart functionality
  - Cash payment processing with change calculation
  - Card payment integration (Square/Stripe support)
  - Receipt generation (HTML/PDF/Text formats)
  - End-of-day reconciliation

- **Reporting and Analytics**
  - Daily sales summary reports
  - Inventory reports with valuation
  - Donation tracking reports
  - CSV export functionality

- **User Management**
  - Role-based permissions (Admin/Volunteer)
  - Secure authentication
  - User activity tracking

## Installation

### Requirements

- Python 3.8+
- SQLite 3

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
cd src
python init_database.py
```

This creates `charity_pos.db` with sample data and default users:
- **Admin**: username=`admin`, password=`admin123`
- **Volunteer**: username=`volunteer`, password=`volunteer123`

**IMPORTANT: Change default passwords in production!**

## Usage

### Quick Launch (Recommended)

**PowerShell:**
```powershell
.\launch.ps1
```

**Batch File:**
```cmd
launch.bat
```

**Or double-click:** `launch.bat`

These scripts automatically:
- Check dependencies
- Create database if needed
- Launch the application

### Manual Launch

```bash
cd src
python main.py
```

### Login

Use the default credentials (admin/admin123 or volunteer/volunteer123) to log in.

### Process a Sale

1. Select "Process Sale" from main menu
2. Add items to cart by searching for them
3. Review cart
4. Complete sale with cash or card payment
5. Receipt is automatically generated

### Manage Inventory

1. Select "Manage Inventory" from main menu
2. Search for existing items
3. Add new items (Admin only)
4. View inventory summary

### Generate Reports

1. Select "Generate Reports" from main menu (Admin only)
2. Choose report type:
   - Daily Sales Report
   - Inventory Report
   - Donation Report

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=src tests/
```

## Database Backup

### Manual Backup

```bash
cd src
python backup_database.py
```

### Automated Backup

The backup script supports automated backups suitable for scheduling:

```python
from backup_database import automated_backup
automated_backup(keep_count=10)
```

Backups are stored in the `backups/` directory.

## Project Structure

```
spec_charity_pos/
├── src/
│   ├── database.py              # Database models and management
│   ├── init_database.py         # Database initialization script
│   ├── backup_database.py       # Database backup utility
│   ├── inventory.py             # Inventory management
│   ├── cart.py                  # Shopping cart
│   ├── payment_processor.py     # Payment processing
│   ├── receipt_generator.py     # Receipt generation
│   ├── reports.py               # Reporting and analytics
│   ├── auth.py                  # Authentication
│   └── main.py                  # Main application
├── tests/
│   ├── test_inventory.py        # Inventory tests
│   ├── test_cart.py             # Cart tests
│   └── test_payment.py          # Payment tests
├── receipts/                    # Generated receipts
├── reports/                     # Generated reports
├── backups/                     # Database backups
├── requirements.txt             # Python dependencies
├── DATABASE_SCHEMA.md           # Database schema documentation
└── README.md                    # This file
```

## Configuration

### Payment Processing

To enable real card payments:

1. Sign up for Square or Stripe
2. Update the API key in `payment_processor.py`
3. Set `test_mode=False` in `CardPaymentProcessor`

### Shop Information

Update shop details in `receipt_generator.py`:

```python
receipt_generator = ReceiptGenerator(
    shop_name="Your Charity Shop Name",
    shop_address="Your Address",
    shop_phone="Your Phone",
    charity_number="Your Charity Number"
)
```

## Security Considerations

- Default passwords must be changed immediately
- Database file should have restricted permissions
- Payment information is never logged
- Use HTTPS for any web-based deployment
- Regular backups are essential

## License

This software is provided for use by charitable organisations.

## Support

For issues or questions, please contact the development team.

---

**Built with the SPEC System**  
Project DNA: TGCAATGC  
Project: charity-pos  
Generated: 2025-11-02

