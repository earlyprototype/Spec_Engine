"""
Task 1, Step 1.4: Store all transactions in database
Primary method: SQLite database
Backup: CSV file if database fails
"""

import sqlite3
import csv
from datetime import datetime, date
from typing import Dict, List, Optional
from pathlib import Path
import json

class TransactionDatabase:
    """Handles persistent storage of all transactions"""
    
    def __init__(self, db_path: str = "transactions.db", backup_csv: str = "transactions_backup.csv"):
        self.db_path = db_path
        self.backup_csv = backup_csv
        self.connection = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            
            # Create transactions table per spec
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    status TEXT NOT NULL,
                    tendered REAL,
                    change_given REAL,
                    description TEXT,
                    receipt_printed INTEGER DEFAULT 0
                )
            """)
            
            self.connection.commit()
            print(f"✓ Database initialized: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"⚠ Database initialization failed: {e}")
            print(f"  Backup mode: Will use CSV file {self.backup_csv}")
    
    def store_transaction(self, transaction: Dict) -> bool:
        """
        Step 1.4: Store transaction
        Primary: SQLite database
        Backup: CSV file
        """
        try:
            # Primary method: SQLite
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO transactions 
                    (transaction_id, timestamp, amount, payment_method, status, tendered, change_given, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    transaction.get('transaction_id'),
                    transaction.get('timestamp'),
                    transaction.get('amount'),
                    transaction.get('payment_method'),
                    'completed' if transaction.get('success') else 'failed',
                    transaction.get('tendered'),
                    transaction.get('change'),
                    transaction.get('description', '')
                ))
                self.connection.commit()
                return True
            else:
                raise sqlite3.Error("No database connection")
                
        except sqlite3.Error as e:
            # Backup method: CSV file
            print(f"⚠ Database write failed: {e}")
            print(f"  Using backup: {self.backup_csv}")
            return self._store_to_csv(transaction)
    
    def _store_to_csv(self, transaction: Dict) -> bool:
        """Backup method: Store to CSV file"""
        try:
            csv_path = Path(self.backup_csv)
            file_exists = csv_path.exists()
            
            with open(csv_path, 'a', newline='') as csvfile:
                fieldnames = ['transaction_id', 'timestamp', 'amount', 'payment_method', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'transaction_id': transaction.get('transaction_id'),
                    'timestamp': transaction.get('timestamp'),
                    'amount': transaction.get('amount'),
                    'payment_method': transaction.get('payment_method'),
                    'status': 'completed' if transaction.get('success') else 'failed'
                })
            
            return True
        except Exception as e:
            print(f"✗ Backup CSV write failed: {e}")
            return False
    
    def get_daily_total(self, target_date: Optional[date] = None) -> float:
        """
        Query: SELECT SUM(amount) WHERE date = today
        Per spec verification requirement
        """
        if target_date is None:
            target_date = date.today()
        
        date_str = target_date.isoformat()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT SUM(amount) as total
                FROM transactions
                WHERE DATE(timestamp) = ?
                AND status = 'completed'
            """, (date_str,))
            
            result = cursor.fetchone()
            return result['total'] if result['total'] else 0.0
            
        except sqlite3.Error as e:
            print(f"✗ Query failed: {e}")
            return 0.0
    
    def get_all_transactions(self, target_date: Optional[date] = None) -> List[Dict]:
        """Get all transactions for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        date_str = target_date.isoformat()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM transactions
                WHERE DATE(timestamp) = ?
                ORDER BY timestamp
            """, (date_str,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"✗ Query failed: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


# Verification tests per spec
if __name__ == "__main__":
    print("Running Step 1.4 verification tests...\n")
    
    # Create test database
    test_db = TransactionDatabase(db_path="test_transactions.db")
    
    # Test 1: Store 10 transactions
    print("=== Test 1: Store 10 transactions ===")
    test_transactions = [
        {"transaction_id": f"test_{i}", "timestamp": datetime.now().isoformat(), 
         "amount": 10.00 * i, "payment_method": "cash" if i % 2 == 0 else "card",
         "success": True}
        for i in range(1, 11)
    ]
    
    for txn in test_transactions:
        success = test_db.store_transaction(txn)
        print(f"  Stored {txn['transaction_id']}: {success}")
    
    # Test 2: Query daily total
    print("\n=== Test 2: Query daily total ===")
    expected_total = sum(txn['amount'] for txn in test_transactions)
    actual_total = test_db.get_daily_total()
    print(f"Expected total: £{expected_total:.2f}")
    print(f"Actual total: £{actual_total:.2f}")
    print(f"Match: {abs(expected_total - actual_total) < 0.01}")
    
    # Test 3: Verify no duplicates
    print("\n=== Test 3: Verify no duplicates ===")
    all_txns = test_db.get_all_transactions()
    print(f"Stored: {len(test_transactions)} transactions")
    print(f"Retrieved: {len(all_txns)} transactions")
    print(f"No duplicates: {len(all_txns) == len(test_transactions)}")
    
    test_db.close()
    print("\n✓ Step 1.4 verification complete")
    
    # Cleanup
    Path("test_transactions.db").unlink(missing_ok=True)



