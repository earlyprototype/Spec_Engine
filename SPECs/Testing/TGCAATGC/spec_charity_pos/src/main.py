"""
Charity Shop POS - Main Application
Command-line interface for the POS system
"""

import sys
from decimal import Decimal
from datetime import date
from pathlib import Path

from database import init_database, get_session, User
from inventory import InventoryManager
from cart import ShoppingCart
from payment_processor import PaymentManager, PaymentMethod
from receipt_generator import ReceiptGenerator, ReceiptData
from reports import ReportGenerator
from auth import AuthManager


class CharityPOSApp:
    """Main POS application"""
    
    def __init__(self, db_path='charity_pos.db'):
        """Initialize the POS application"""
        self.db_path = db_path
        self.db_manager = init_database(db_path)
        self.session = self.db_manager.get_session()
        
        self.inventory_manager = InventoryManager(self.session)
        self.payment_manager = PaymentManager()
        self.receipt_generator = ReceiptGenerator()
        self.report_generator = ReportGenerator(self.session)
        self.auth_manager = AuthManager(self.session)
        
        self.current_user = None
        self.cart = ShoppingCart()
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("Charity Shop POS System".center(60))
        print("=" * 60)
        
        # Check if database exists and is initialized
        if not Path(self.db_path).exists():
            print("\n✗ Database not found!")
            print("Please run 'python init_database.py' first to set up the database.")
            return
        
        # Login
        if not self.login():
            print("\nLogin failed. Exiting...")
            return
        
        # Main menu
        while True:
            print("\n" + "=" * 60)
            print(f"Logged in as: {self.current_user.username} ({self.current_user.role})")
            print("=" * 60)
            print("\nMain Menu:")
            print("  1. Process Sale")
            print("  2. Manage Inventory")
            print("  3. Record Donation")
            print("  4. Generate Reports")
            print("  5. View Cart")
            print("  6. Logout")
            print("  7. Exit")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                self.process_sale_menu()
            elif choice == '2':
                self.inventory_menu()
            elif choice == '3':
                self.record_donation_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                self.view_cart()
            elif choice == '6':
                print("\nLogging out...")
                if not self.login():
                    break
            elif choice == '7':
                print("\nThank you for using Charity POS!")
                break
            else:
                print("\n✗ Invalid option. Please select 1-7.")
    
    def login(self) -> bool:
        """Handle user login"""
        print("\n" + "-" * 60)
        print("Login")
        print("-" * 60)
        
        attempts = 3
        while attempts > 0:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            user = self.auth_manager.authenticate(username, password)
            if user:
                self.current_user = user
                print(f"\n✓ Login successful! Welcome, {user.username}.")
                return True
            
            attempts -= 1
            if attempts > 0:
                print(f"\n✗ Invalid credentials. {attempts} attempt(s) remaining.")
            else:
                print("\n✗ Login failed. Too many attempts.")
                return False
        
        return False
    
    def process_sale_menu(self):
        """Process a sale"""
        print("\n" + "-" * 60)
        print("Process Sale")
        print("-" * 60)
        
        while True:
            print("\n1. Add item to cart")
            print("2. View cart")
            print("3. Complete sale")
            print("4. Clear cart")
            print("5. Back to main menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.add_item_to_cart()
            elif choice == '2':
                self.view_cart()
            elif choice == '3':
                if self.complete_sale():
                    break
            elif choice == '4':
                self.cart.clear()
                print("\n✓ Cart cleared.")
            elif choice == '5':
                break
    
    def add_item_to_cart(self):
        """Add item to cart"""
        query = input("\nSearch for item (name/SKU): ").strip()
        
        if not query:
            return
        
        items = self.inventory_manager.search_items(query, in_stock_only=True)
        
        if not items:
            print("\n✗ No items found.")
            return
        
        print(f"\nFound {len(items)} item(s):")
        for i, item in enumerate(items[:10], 1):
            print(f"  {i}. {item.name} - £{item.price} (Stock: {item.stock_quantity})")
        
        try:
            selection = int(input("\nSelect item number (0 to cancel): "))
            if selection == 0:
                return
            if 1 <= selection <= len(items):
                item = items[selection - 1]
                qty = int(input(f"Quantity (max {item.stock_quantity}): ") or "1")
                
                if qty > item.stock_quantity:
                    print(f"\n✗ Only {item.stock_quantity} in stock.")
                    return
                
                self.cart.add_item(item.id, item.name, item.price, qty)
                print(f"\n✓ Added {qty} x {item.name} to cart.")
            else:
                print("\n✗ Invalid selection.")
        except ValueError:
            print("\n✗ Invalid input.")
    
    def view_cart(self):
        """Display current cart"""
        print("\n" + "-" * 60)
        print(self.cart)
        print("-" * 60)
    
    def complete_sale(self) -> bool:
        """Complete the sale"""
        if self.cart.is_empty():
            print("\n✗ Cart is empty.")
            return False
        
        self.view_cart()
        
        print("\nPayment Method:")
        print("  1. Cash")
        print("  2. Card")
        
        choice = input("\nSelect (1-2): ").strip()
        
        if choice == '1':
            return self.process_cash_payment()
        elif choice == '2':
            return self.process_card_payment()
        else:
            print("\n✗ Invalid payment method.")
            return False
    
    def process_cash_payment(self) -> bool:
        """Process cash payment"""
        total = self.cart.get_total()
        
        try:
            cash_given = Decimal(input(f"\nTotal: £{total:.2f}\nCash given: £"))
            
            result = self.payment_manager.process_payment(
                PaymentMethod.CASH,
                total,
                cash_given=cash_given
            )
            
            if result.success:
                change = result.payment_data.get('change', 0)
                print(f"\n✓ Payment successful!")
                print(f"   Change: £{change:.2f}")
                
                # Generate receipt
                self.generate_receipt('cash', cash_given, Decimal(str(change)))
                self.cart.clear()
                return True
            else:
                print(f"\n✗ Payment failed: {result.message}")
                return False
        
        except (ValueError, Exception) as e:
            print(f"\n✗ Error: {e}")
            return False
    
    def process_card_payment(self) -> bool:
        """Process card payment"""
        total = self.cart.get_total()
        
        print(f"\nTotal: £{total:.2f}")
        print("Processing card payment...")
        
        result = self.payment_manager.process_payment(
            PaymentMethod.CARD,
            total,
            card_token="test_card"
        )
        
        if result.success:
            print(f"\n✓ Payment successful!")
            print(f"   Transaction ID: {result.transaction_id}")
            
            # Generate receipt
            self.generate_receipt('card')
            self.cart.clear()
            return True
        else:
            print(f"\n✗ Payment failed: {result.message}")
            return False
    
    def generate_receipt(self, payment_method: str, cash_given: Decimal = None,
                        change: Decimal = None):
        """Generate and save receipt"""
        receipt_data = ReceiptData(
            transaction_id=1,  # Would be actual transaction ID
            items=[
                {
                    'name': item.name,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'subtotal': item.subtotal
                }
                for item in self.cart.get_all_items()
            ],
            total=self.cart.get_total(),
            payment_method=payment_method,
            cash_given=cash_given,
            change=change,
            cashier=self.current_user.username if self.current_user else "Staff"
        )
        
        # Save receipt
        receipt_path = self.receipt_generator.save_receipt(receipt_data, format='html')
        print(f"\n✓ Receipt saved: {receipt_path}")
    
    def inventory_menu(self):
        """Inventory management menu"""
        print("\n" + "-" * 60)
        print("Inventory Management")
        print("-" * 60)
        print("\n1. Search items")
        print("2. Add new item")
        print("3. View inventory summary")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            self.search_items()
        elif choice == '2':
            self.add_new_item()
        elif choice == '3':
            summary = self.inventory_manager.get_inventory_summary()
            print("\nInventory Summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")
        elif choice == '4':
            return
    
    def search_items(self):
        """Search and display items"""
        query = input("\nSearch query: ").strip()
        items = self.inventory_manager.search_items(query)
        
        if not items:
            print("\n✗ No items found.")
            return
        
        print(f"\nFound {len(items)} item(s):")
        for item in items[:20]:
            print(f"  {item.name} - £{item.price} (Stock: {item.stock_quantity})")
    
    def add_new_item(self):
        """Add new item to inventory"""
        if self.current_user.role != 'admin':
            print("\n✗ Admin access required.")
            return
        
        try:
            name = input("\nItem name: ").strip()
            price = Decimal(input("Price: £"))
            stock = int(input("Stock quantity: "))
            
            item = self.inventory_manager.add_item(name, price, stock_quantity=stock)
            print(f"\n✓ Item added: {item}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def record_donation_menu(self):
        """Record a donation"""
        print("\n" + "-" * 60)
        print("Record Donation")
        print("-" * 60)
        
        donor_name = input("\nDonor name (optional): ").strip() or None
        donor_contact = input("Donor contact (optional): ").strip() or None
        notes = input("Notes (optional): ").strip() or None
        
        try:
            donation = self.inventory_manager.add_donation(
                donor_name=donor_name,
                donor_contact=donor_contact,
                notes=notes
            )
            print(f"\n✓ Donation recorded: ID {donation.id}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def reports_menu(self):
        """Reports menu"""
        if self.current_user.role != 'admin':
            print("\n✗ Admin access required for reports.")
            return
        
        print("\n" + "-" * 60)
        print("Reports")
        print("-" * 60)
        print("\n1. Daily Sales Report")
        print("2. Inventory Report")
        print("3. Donation Report")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            print(self.report_generator.format_daily_sales_report())
        elif choice == '2':
            print(self.report_generator.format_inventory_report())
        elif choice == '3':
            print(self.report_generator.format_donation_report())
        elif choice == '4':
            return


def main():
    """Main entry point"""
    app = CharityPOSApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Exiting...")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if app.session:
            app.session.close()


if __name__ == '__main__':
    main()



