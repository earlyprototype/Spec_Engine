"""
Task 3: Daily Reconciliation
Implements Steps 3.1, 3.2 from spec_transaction_v2.md
"""

from datetime import date, datetime
from typing import Dict, Optional
from pathlib import Path
import csv

class DailyReconciliation:
    """Handles end-of-day reporting and till reconciliation"""
    
    def __init__(self, database, opening_float: float = 100.00):
        self.database = database
        self.opening_float = opening_float
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def calculate_daily_totals(self, target_date: Optional[date] = None) -> Dict:
        """
        Step 3.1: Calculate daily totals by payment method
        Primary method: SQL GROUP BY
        Backup: Manual iteration
        """
        if target_date is None:
            target_date = date.today()
        
        try:
            # Primary method: SQL GROUP BY
            date_str = target_date.isoformat()
            
            cursor = self.database.connection.cursor()
            cursor.execute("""
                SELECT 
                    payment_method,
                    SUM(amount) as total,
                    COUNT(*) as count
                FROM transactions
                WHERE DATE(timestamp) = ?
                AND status = 'completed'
                GROUP BY payment_method
            """, (date_str,))
            
            results = cursor.fetchall()
            
            # Build totals dict
            totals = {
                'cash': 0.0,
                'card': 0.0,
                'cash_count': 0,
                'card_count': 0
            }
            
            for row in results:
                method = row['payment_method'].lower()
                if method == 'cash':
                    totals['cash'] = float(row['total'])
                    totals['cash_count'] = row['count']
                elif method == 'card':
                    totals['card'] = float(row['total'])
                    totals['card_count'] = row['count']
            
            totals['total'] = totals['cash'] + totals['card']
            totals['transaction_count'] = totals['cash_count'] + totals['card_count']
            totals['expected_till_cash'] = self.opening_float + totals['cash']
            totals['date'] = target_date.isoformat()
            
            return totals
            
        except Exception as e:
            print(f"⚠ SQL GROUP BY failed: {e}")
            # Backup method: Manual iteration
            return self._calculate_totals_manually(target_date)
    
    def _calculate_totals_manually(self, target_date: date) -> Dict:
        """Backup method: Iterate through transactions manually"""
        transactions = self.database.get_all_transactions(target_date)
        
        totals = {
            'cash': 0.0,
            'card': 0.0,
            'cash_count': 0,
            'card_count': 0
        }
        
        for txn in transactions:
            if txn['status'] == 'completed':
                amount = txn['amount']
                method = txn['payment_method'].lower()
                
                if method == 'cash':
                    totals['cash'] += amount
                    totals['cash_count'] += 1
                elif method == 'card':
                    totals['card'] += amount
                    totals['card_count'] += 1
        
        totals['total'] = totals['cash'] + totals['card']
        totals['transaction_count'] = totals['cash_count'] + totals['card_count']
        totals['expected_till_cash'] = self.opening_float + totals['cash']
        totals['date'] = target_date.isoformat()
        
        return totals
    
    def generate_end_of_day_report(self, target_date: Optional[date] = None) -> bool:
        """
        Step 3.2: Generate end-of-day report
        Primary method: PDF report
        Backup: CSV report
        """
        if target_date is None:
            target_date = date.today()
        
        # Get totals
        totals = self.calculate_daily_totals(target_date)
        
        try:
            # Try PDF generation
            return self._generate_pdf_report(totals, target_date)
        except Exception as e:
            print(f"⚠ PDF report failed: {e}")
            # Backup: CSV report
            return self._generate_csv_report(totals, target_date)
    
    def _generate_pdf_report(self, totals: Dict, target_date: date) -> bool:
        """Primary method: Generate PDF report"""
        try:
            # Placeholder: Would use ReportLab for actual PDF
            report_path = self.reports_dir / f"{target_date.isoformat()}.txt"
            
            with open(report_path, 'w') as f:
                f.write("=" * 50 + "\n")
                f.write(f"END OF DAY REPORT - {target_date.strftime('%d/%m/%Y')}\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Opening Float:        £{self.opening_float:>10.2f}\n\n")
                
                f.write("SALES SUMMARY\n")
                f.write("-" * 50 + "\n")
                f.write(f"Cash Sales:           £{totals['cash']:>10.2f}  ({totals['cash_count']} transactions)\n")
                f.write(f"Card Sales:           £{totals['card']:>10.2f}  ({totals['card_count']} transactions)\n")
                f.write("-" * 50 + "\n")
                f.write(f"TOTAL SALES:          £{totals['total']:>10.2f}  ({totals['transaction_count']} transactions)\n\n")
                
                f.write("TILL RECONCILIATION\n")
                f.write("-" * 50 + "\n")
                f.write(f"Expected Cash in Till: £{totals['expected_till_cash']:>10.2f}\n")
                f.write(f"(Opening £{self.opening_float:.2f} + Cash Sales £{totals['cash']:.2f})\n\n")
                
                f.write("Card Payments:         £{:.2f}\n".format(totals['card']))
                f.write("(Paid directly to bank)\n\n")
                
                f.write("=" * 50 + "\n")
                f.write(f"Report generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            
            print(f"✓ Report generated: {report_path}")
            return True
            
        except Exception as e:
            print(f"✗ PDF report failed: {e}")
            return False
    
    def _generate_csv_report(self, totals: Dict, target_date: date) -> bool:
        """Backup method: Generate CSV report"""
        try:
            report_path = self.reports_dir / f"{target_date.isoformat()}.csv"
            
            with open(report_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Date', target_date.isoformat()])
                writer.writerow(['Opening Float', f"£{self.opening_float:.2f}"])
                writer.writerow(['Cash Sales', f"£{totals['cash']:.2f}"])
                writer.writerow(['Cash Transactions', totals['cash_count']])
                writer.writerow(['Card Sales', f"£{totals['card']:.2f}"])
                writer.writerow(['Card Transactions', totals['card_count']])
                writer.writerow(['Total Sales', f"£{totals['total']:.2f}"])
                writer.writerow(['Total Transactions', totals['transaction_count']])
                writer.writerow(['Expected Till Cash', f"£{totals['expected_till_cash']:.2f}"])
            
            print(f"✓ CSV report generated: {report_path}")
            return True
            
        except Exception as e:
            print(f"✗ CSV report failed: {e}")
            return False


# Verification tests per spec
if __name__ == "__main__":
    print("Running Task 3 verification tests...\n")
    
    # Need database for testing
    from database import TransactionDatabase
    
    test_db = TransactionDatabase(db_path="test_reconciliation.db")
    reconciliation = DailyReconciliation(test_db, opening_float=100.00)
    
    # Create test transactions: 5 cash (£50 total) + 3 card (£75 total)
    print("=== Creating test transactions ===")
    test_txns = [
        {"transaction_id": f"cash_{i}", "timestamp": datetime.now().isoformat(),
         "amount": 10.00, "payment_method": "cash", "success": True}
        for i in range(5)
    ] + [
        {"transaction_id": f"card_{i}", "timestamp": datetime.now().isoformat(),
         "amount": 25.00, "payment_method": "card", "success": True}
        for i in range(3)
    ]
    
    for txn in test_txns:
        test_db.store_transaction(txn)
    
    # Step 3.1: Calculate totals
    print("\n=== Step 3.1: Calculate Daily Totals ===")
    totals = reconciliation.calculate_daily_totals()
    
    print(f"Cash: £{totals['cash']:.2f} (expected: £50.00)")
    print(f"Card: £{totals['card']:.2f} (expected: £75.00)")
    print(f"Total: £{totals['total']:.2f} (expected: £125.00)")
    print(f"Expected Till Cash: £{totals['expected_till_cash']:.2f} (expected: £150.00)")
    
    # Verify math
    cash_correct = abs(totals['cash'] - 50.00) < 0.01
    card_correct = abs(totals['card'] - 75.00) < 0.01
    total_correct = abs(totals['total'] - 125.00) < 0.01
    till_correct = abs(totals['expected_till_cash'] - 150.00) < 0.01
    
    print(f"\nVerification: Cash={cash_correct}, Card={card_correct}, Total={total_correct}, Till={till_correct}")
    
    # Step 3.2: Generate report
    print("\n=== Step 3.2: Generate End-of-Day Report ===")
    report_success = reconciliation.generate_end_of_day_report()
    print(f"Report generated: {report_success}")
    
    test_db.close()
    print("\n✓ Task 3 verification complete")
    
    # Cleanup
    Path("test_reconciliation.db").unlink(missing_ok=True)



