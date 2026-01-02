"""
Charity Shop Point-of-Sale System
Main integration and GUI
Built per spec_transaction_v2.md
"""

from payment_processor import PaymentProcessor
from database import TransactionDatabase
from receipt_generator import ReceiptGenerator
from reconciliation import DailyReconciliation
from datetime import datetime
import json
from pathlib import Path

class CharityPoS:
    """Main point-of-sale system integration"""
    
    def __init__(self):
        self.payment_processor = PaymentProcessor(test_mode=True)
        self.database = TransactionDatabase()
        self.receipt_generator = ReceiptGenerator()
        self.reconciliation = DailyReconciliation(self.database)
        self.progress_log = []
    
    def process_sale(self, amount: float, payment_method: str, description: str = "Sale", 
                     tendered: float = None) -> dict:
        """Process a complete sale: payment → database → receipt"""
        
        # Task 1: Process payment
        if payment_method.lower() == 'card':
            result = self.payment_processor.process_card_payment(amount, description)
        elif payment_method.lower() == 'cash':
            if tendered is None:
                tendered = amount
            result = self.payment_processor.process_cash_payment(amount, tendered)
        else:
            return {"success": False, "error": "Invalid payment method"}
        
        if not result['success']:
            self._log_step("payment_failed", result)
            return result
        
        self._log_step("payment_completed", result)
        
        # Step 1.4: Store transaction
        stored = self.database.store_transaction(result)
        if not stored:
            self._log_step("storage_failed", {"transaction_id": result['transaction_id']})
            # CRITICAL: Cannot continue without transaction record
            return {"success": False, "error": "Failed to store transaction"}
        
        self._log_step("storage_completed", {"transaction_id": result['transaction_id']})
        
        # Task 2: Generate and print receipt
        receipt_text = self.receipt_generator.format_receipt(result)
        result['receipt'] = receipt_text
        
        # Step 2.2: Generate PDF (non-critical)
        pdf_success = self.receipt_generator.generate_pdf(result)
        self._log_step("pdf_generation", {"success": pdf_success, "transaction_id": result['transaction_id']})
        
        # Step 2.3: Print receipt (non-critical)
        print_success = self.receipt_generator.print_receipt(receipt_text)
        result['printed'] = print_success
        self._log_step("receipt_printed", {"success": print_success, "transaction_id": result['transaction_id']})
        
        return result
    
    def end_of_day(self):
        """Run end-of-day reconciliation"""
        print("\n" + "=" * 60)
        print("END OF DAY RECONCILIATION")
        print("=" * 60 + "\n")
        
        # Task 3: Calculate totals and generate report
        totals = self.reconciliation.calculate_daily_totals()
        
        print(f"Cash Sales:    £{totals['cash']:.2f} ({totals['cash_count']} transactions)")
        print(f"Card Sales:    £{totals['card']:.2f} ({totals['card_count']} transactions)")
        print(f"Total Sales:   £{totals['total']:.2f} ({totals['transaction_count']} transactions)")
        print(f"\nExpected Till Cash: £{totals['expected_till_cash']:.2f}")
        print(f"(Opening float £{self.reconciliation.opening_float:.2f} + Cash sales £{totals['cash']:.2f})")
        
        # Generate report
        report_success = self.reconciliation.generate_end_of_day_report()
        
        if report_success:
            print(f"\n✓ End-of-day report generated")
        else:
            print(f"\n⚠ Report generation failed")
        
        self._log_step("end_of_day_complete", totals)
        
        return totals
    
    def _log_step(self, step_name: str, data: dict):
        """Log to progress_transaction_v2.json"""
        log_entry = {
            "step": step_name,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.progress_log.append(log_entry)
    
    def save_progress_log(self):
        """Save execution progress log"""
        log_path = Path("progress_transaction_v2.json")
        
        progress_data = {
            "dna_code": "TGCAATGC",
            "spec_id": "transaction_v2",
            "execution_mode": "dynamic",
            "start_time": self.progress_log[0]['timestamp'] if self.progress_log else None,
            "end_time": datetime.now().isoformat(),
            "steps": self.progress_log
        }
        
        with open(log_path, 'w') as f:
            json.dump(progress_data, f, indent=2)
        
        print(f"\n✓ Progress log saved: {log_path}")


def main():
    """Demo: Run complete system test"""
    print("=" * 60)
    print("CHARITY SHOP POS SYSTEM - FULL INTEGRATION TEST")
    print("=" * 60 + "\n")
    
    pos = CharityPoS()
    
    # Test transactions
    print("Processing test transactions...\n")
    
    # Cash sales
    sale1 = pos.process_sale(15.99, 'cash', 'Vintage scarf', tendered=20.00)
    print(f"Sale 1 (Cash): {'✓' if sale1['success'] else '✗'} - £{sale1.get('amount', 0):.2f}")
    
    sale2 = pos.process_sale(5.50, 'cash', 'Coffee mug', tendered=10.00)
    print(f"Sale 2 (Cash): {'✓' if sale2['success'] else '✗'} - £{sale2.get('amount', 0):.2f}")
    
    sale3 = pos.process_sale(8.00, 'cash', 'Book set', tendered=10.00)
    print(f"Sale 3 (Cash): {'✓' if sale3['success'] else '✗'} - £{sale3.get('amount', 0):.2f}")
    
    # Card sales
    sale4 = pos.process_sale(25.00, 'card', 'Coat')
    print(f"Sale 4 (Card): {'✓' if sale4['success'] else '✗'} - £{sale4.get('amount', 0):.2f}")
    
    sale5 = pos.process_sale(12.50, 'card', 'Handbag')
    print(f"Sale 5 (Card): {'✓' if sale5['success'] else '✗'} - £{sale5.get('amount', 0):.2f}")
    
    # Run end-of-day
    totals = pos.end_of_day()
    
    # Save progress log
    pos.save_progress_log()
    
    print("\n" + "=" * 60)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 60)
    print(f"\nTotal transactions: {totals['transaction_count']}")
    print(f"Total sales: £{totals['total']:.2f}")
    print(f"System status: OPERATIONAL")


if __name__ == "__main__":
    main()



