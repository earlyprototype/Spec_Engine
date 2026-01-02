# Charity Shop POS - Database Schema

## Entity Relationship Diagram

```
+----------------+       +------------------+       +----------------+
|    Users       |       |   Transactions   |       |     Items      |
+----------------+       +------------------+       +----------------+
| id (PK)        |       | id (PK)          |       | id (PK)        |
| username       |  1..* | timestamp        | *..* | name           |
| password_hash  |<------| user_id (FK)     |----->| description    |
| role           |       | payment_method   |   |  | price          |
| created_at     |       | total_amount     |   |  | category_id(FK)|
+----------------+       | cash_given       |   |  | stock_quantity |
                         | change_returned  |   |  | sku            |
                         | status           |   |  | donation_id(FK)|
                         +------------------+   |  | created_at     |
                                  |             |  +----------------+
                                  |             |           |
                                  v             |           v
                         +------------------+   |  +----------------+
                         | TransactionItems |---+  |   Categories   |
                         +------------------+      +----------------+
                         | id (PK)          |      | id (PK)        |
                         | transaction_id   |      | name           |
                         | item_id (FK)     |      | parent_id (FK) |
                         | quantity         |      | description    |
                         | unit_price       |      +----------------+
                         | subtotal         |
                         +------------------+
                         
+----------------+       +------------------+
|   Donations    |       |     Receipts     |
+----------------+       +------------------+
| id (PK)        |       | id (PK)          |
| donor_name     |       | transaction_id   |
| donor_contact  |  1..* | receipt_number   |
| donation_date  |<------| generated_at     |
| total_value    |       | format           |
| notes          |       | file_path        |
+----------------+       +------------------+
```

## Table Definitions

### Users
Manages staff and volunteer accounts with role-based permissions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | User login name |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| role | VARCHAR(20) | NOT NULL | 'admin' or 'volunteer' |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

### Items
Inventory items available for sale in the charity shop.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique item identifier |
| name | VARCHAR(100) | NOT NULL | Item name |
| description | TEXT | NULL | Detailed item description |
| price | DECIMAL(10,2) | NOT NULL | Sale price |
| category_id | INTEGER | FOREIGN KEY(Categories.id) | Item category |
| stock_quantity | INTEGER | DEFAULT 1 | Current stock level |
| sku | VARCHAR(50) | UNIQUE, NULL | Stock keeping unit code |
| donation_id | INTEGER | FOREIGN KEY(Donations.id), NULL | Source donation if applicable |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Item creation timestamp |

### Categories
Hierarchical categorisation system for inventory items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique category identifier |
| name | VARCHAR(50) | NOT NULL | Category name |
| parent_id | INTEGER | FOREIGN KEY(Categories.id), NULL | Parent category for hierarchy |
| description | TEXT | NULL | Category description |

### Transactions
Records of all sales transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique transaction identifier |
| timestamp | DATETIME | DEFAULT CURRENT_TIMESTAMP | Transaction timestamp |
| user_id | INTEGER | FOREIGN KEY(Users.id), NOT NULL | Staff member who processed sale |
| payment_method | VARCHAR(20) | NOT NULL | 'cash', 'card', 'other' |
| total_amount | DECIMAL(10,2) | NOT NULL | Total transaction amount |
| cash_given | DECIMAL(10,2) | NULL | Cash amount provided by customer |
| change_returned | DECIMAL(10,2) | NULL | Change given to customer |
| status | VARCHAR(20) | DEFAULT 'completed' | 'completed', 'cancelled', 'refunded' |

### TransactionItems
Line items linking items to transactions (many-to-many).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique line item identifier |
| transaction_id | INTEGER | FOREIGN KEY(Transactions.id), NOT NULL | Parent transaction |
| item_id | INTEGER | FOREIGN KEY(Items.id), NOT NULL | Sold item |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | Quantity sold |
| unit_price | DECIMAL(10,2) | NOT NULL | Price per unit at time of sale |
| subtotal | DECIMAL(10,2) | NOT NULL | quantity * unit_price |

### Donations
Records of items donated to the charity shop.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique donation identifier |
| donor_name | VARCHAR(100) | NULL | Name of donor |
| donor_contact | VARCHAR(100) | NULL | Contact information |
| donation_date | DATE | DEFAULT CURRENT_DATE | Date donation received |
| total_value | DECIMAL(10,2) | NULL | Estimated total value |
| notes | TEXT | NULL | Additional notes about donation |

### Receipts
Generated receipts for transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique receipt identifier |
| transaction_id | INTEGER | FOREIGN KEY(Transactions.id), UNIQUE | Associated transaction |
| receipt_number | VARCHAR(50) | UNIQUE, NOT NULL | Human-readable receipt number |
| generated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Receipt generation timestamp |
| format | VARCHAR(10) | NOT NULL | 'html', 'pdf', 'text' |
| file_path | VARCHAR(255) | NULL | Path to saved receipt file |

## Indexes

```sql
-- Performance indexes for common queries
CREATE INDEX idx_items_category ON Items(category_id);
CREATE INDEX idx_items_sku ON Items(sku);
CREATE INDEX idx_transactions_user ON Transactions(user_id);
CREATE INDEX idx_transactions_timestamp ON Transactions(timestamp);
CREATE INDEX idx_transactions_status ON Transactions(status);
CREATE INDEX idx_transaction_items_transaction ON TransactionItems(transaction_id);
CREATE INDEX idx_transaction_items_item ON TransactionItems(item_id);
CREATE INDEX idx_donations_date ON Donations(donation_date);
CREATE INDEX idx_receipts_transaction ON Receipts(transaction_id);
```

## Business Rules

1. **Stock Management**
   - Stock quantity decrements when item added to completed transaction
   - Stock quantity increments if transaction cancelled/refunded
   - Alert when stock_quantity reaches 0 or configured threshold

2. **Transaction Integrity**
   - Transaction total must equal sum of TransactionItems subtotals
   - Cash transactions must have cash_given >= total_amount
   - change_returned = cash_given - total_amount for cash transactions

3. **User Permissions**
   - Admin: full access to all functions including user management, reports, reconciliation
   - Volunteer: access to sales, inventory viewing, donation recording (limited edit permissions)

4. **Audit Trail**
   - All transactions immutable once completed
   - Cancellations/refunds create new transaction records
   - All timestamps recorded in UTC

5. **Data Retention**
   - Transaction records retained indefinitely for financial audit
   - User activity logged for security
   - Backup created daily of complete database

## Schema Version
- Version: 1.0
- Created: 2025-11-02
- Compatible with: SQLite 3.x, PostgreSQL 12+, MySQL 8+



