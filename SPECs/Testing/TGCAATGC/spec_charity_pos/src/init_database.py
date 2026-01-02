"""
Charity Shop POS - Database Initialization
Creates database schema and populates with seed data
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal
import hashlib

# Import database models
from database import (
    init_database, User, Category, Item, Donation,
    Transaction, TransactionItem, Receipt
)


def hash_password(password):
    """Simple password hashing (in production, use bcrypt)"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_seed_data(session):
    """Create initial seed data for the database"""
    
    print("Creating seed data...")
    
    # 1. Create Users
    print("\n1. Creating users...")
    admin_user = User(
        username='admin',
        password_hash=hash_password('admin123'),  # Change in production!
        role='admin'
    )
    
    volunteer_user = User(
        username='volunteer',
        password_hash=hash_password('volunteer123'),  # Change in production!
        role='volunteer'
    )
    
    session.add_all([admin_user, volunteer_user])
    session.commit()
    print(f"   Created: {admin_user}")
    print(f"   Created: {volunteer_user}")
    
    # 2. Create Categories
    print("\n2. Creating categories...")
    categories = [
        Category(name='Books', description='Books of all genres'),
        Category(name='Clothing', description='Clothing and accessories'),
        Category(name='Electronics', description='Electronic devices and gadgets'),
        Category(name='Furniture', description='Furniture and home items'),
        Category(name='Toys', description='Toys and games'),
        Category(name='Kitchen', description='Kitchenware and utensils'),
        Category(name='Media', description='CDs, DVDs, and vinyl records'),
        Category(name='Miscellaneous', description='Other items'),
    ]
    
    for cat in categories:
        session.add(cat)
    session.commit()
    
    for cat in categories:
        print(f"   Created: {cat}")
    
    # 3. Create a sample donation
    print("\n3. Creating sample donation...")
    donation1 = Donation(
        donor_name='John Smith',
        donor_contact='john.smith@example.com',
        donation_date=date.today() - timedelta(days=7),
        total_value=Decimal('125.00'),
        notes='Box of books and kitchen items'
    )
    
    session.add(donation1)
    session.commit()
    print(f"   Created: {donation1}")
    
    # 4. Create Items
    print("\n4. Creating sample items...")
    items = [
        # Books
        Item(name='The Great Gatsby', description='Classic novel by F. Scott Fitzgerald',
             price=Decimal('3.50'), category_id=1, stock_quantity=2, sku='BOOK001', donation_id=1),
        Item(name='Python Programming Guide', description='Learn Python programming',
             price=Decimal('8.00'), category_id=1, stock_quantity=1, sku='BOOK002'),
        Item(name='Cookbook Collection', description='Set of 3 cookbooks',
             price=Decimal('12.00'), category_id=1, stock_quantity=1, sku='BOOK003', donation_id=1),
        
        # Clothing
        Item(name='Winter Coat', description='Warm winter coat, size L',
             price=Decimal('25.00'), category_id=2, stock_quantity=1, sku='CLO001'),
        Item(name='Designer Jeans', description='Levi\'s jeans, size 32',
             price=Decimal('15.00'), category_id=2, stock_quantity=2, sku='CLO002'),
        
        # Electronics
        Item(name='Digital Clock Radio', description='AM/FM radio with alarm',
             price=Decimal('10.00'), category_id=3, stock_quantity=1, sku='ELEC001'),
        Item(name='USB Cables Set', description='Set of 5 USB charging cables',
             price=Decimal('5.00'), category_id=3, stock_quantity=3, sku='ELEC002'),
        
        # Furniture
        Item(name='Wooden Chair', description='Solid wood dining chair',
             price=Decimal('20.00'), category_id=4, stock_quantity=4, sku='FURN001'),
        Item(name='Table Lamp', description='Bedside table lamp',
             price=Decimal('12.00'), category_id=4, stock_quantity=2, sku='FURN002'),
        
        # Toys
        Item(name='Board Game - Monopoly', description='Classic Monopoly board game',
             price=Decimal('8.00'), category_id=5, stock_quantity=1, sku='TOY001'),
        Item(name='Teddy Bear', description='Soft plush teddy bear',
             price=Decimal('5.00'), category_id=5, stock_quantity=3, sku='TOY002'),
        
        # Kitchen
        Item(name='Coffee Maker', description='12-cup coffee maker',
             price=Decimal('18.00'), category_id=6, stock_quantity=1, sku='KITCH001', donation_id=1),
        Item(name='Cutlery Set', description='Set of knives, forks, and spoons',
             price=Decimal('10.00'), category_id=6, stock_quantity=2, sku='KITCH002', donation_id=1),
        
        # Media
        Item(name='Beatles Vinyl Collection', description='3 Beatles albums on vinyl',
             price=Decimal('30.00'), category_id=7, stock_quantity=1, sku='MEDIA001'),
        Item(name='DVD Box Set', description='Complete series DVD collection',
             price=Decimal('15.00'), category_id=7, stock_quantity=1, sku='MEDIA002'),
        
        # Miscellaneous
        Item(name='Picture Frame', description='Wooden picture frame',
             price=Decimal('4.00'), category_id=8, stock_quantity=5, sku='MISC001'),
        Item(name='Vase', description='Decorative ceramic vase',
             price=Decimal('6.00'), category_id=8, stock_quantity=2, sku='MISC002'),
    ]
    
    for item in items:
        session.add(item)
    session.commit()
    
    for item in items:
        print(f"   Created: {item}")
    
    # 5. Create a sample transaction
    print("\n5. Creating sample transaction...")
    transaction1 = Transaction(
        timestamp=datetime.utcnow() - timedelta(hours=2),
        user_id=volunteer_user.id,
        payment_method='cash',
        total_amount=Decimal('16.50'),
        cash_given=Decimal('20.00'),
        change_returned=Decimal('3.50'),
        status='completed'
    )
    
    session.add(transaction1)
    session.commit()
    
    # Add transaction items
    trans_item1 = TransactionItem(
        transaction_id=transaction1.id,
        item_id=1,  # The Great Gatsby
        quantity=1,
        unit_price=Decimal('3.50'),
        subtotal=Decimal('3.50')
    )
    
    trans_item2 = TransactionItem(
        transaction_id=transaction1.id,
        item_id=11,  # Teddy Bear
        quantity=1,
        unit_price=Decimal('5.00'),
        subtotal=Decimal('5.00')
    )
    
    trans_item3 = TransactionItem(
        transaction_id=transaction1.id,
        item_id=2,  # Python Programming Guide
        quantity=1,
        unit_price=Decimal('8.00'),
        subtotal=Decimal('8.00')
    )
    
    session.add_all([trans_item1, trans_item2, trans_item3])
    session.commit()
    
    print(f"   Created: {transaction1}")
    print(f"   Created: {trans_item1}")
    print(f"   Created: {trans_item2}")
    print(f"   Created: {trans_item3}")
    
    # 6. Create receipt for transaction
    print("\n6. Creating sample receipt...")
    receipt1 = Receipt(
        transaction_id=transaction1.id,
        receipt_number=f'RCP-{transaction1.id:06d}',
        generated_at=transaction1.timestamp,
        format='html',
        file_path=f'receipts/receipt_{transaction1.id}.html'
    )
    
    session.add(receipt1)
    session.commit()
    print(f"   Created: {receipt1}")
    
    print("\n✓ Seed data creation completed successfully!")


def main():
    """Main initialization function"""
    print("=" * 60)
    print("Charity Shop POS - Database Initialization")
    print("=" * 60)
    
    # Database file path
    db_path = 'charity_pos.db'
    
    # Check if database already exists
    if Path(db_path).exists():
        response = input(f"\nDatabase '{db_path}' already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Initialization cancelled.")
            return
        
        # Remove existing database
        Path(db_path).unlink()
        print(f"Removed existing database: {db_path}")
    
    # Initialize database
    print(f"\nInitializing database: {db_path}")
    db_manager = init_database(db_path)
    print("✓ Database schema created successfully!")
    
    # Create seed data
    session = db_manager.get_session()
    try:
        create_seed_data(session)
    except Exception as e:
        print(f"\n✗ Error creating seed data: {e}")
        session.rollback()
        raise
    finally:
        session.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("Database Initialization Complete!")
    print("=" * 60)
    print(f"\nDatabase: {db_path}")
    print("\nDefault Users:")
    print("  Admin:     username='admin',     password='admin123'")
    print("  Volunteer: username='volunteer', password='volunteer123'")
    print("\nNOTE: Change default passwords in production!")
    print("\nSample Data:")
    print("  - 8 categories")
    print("  - 17 items")
    print("  - 1 donation record")
    print("  - 1 sample transaction")
    print("  - 1 sample receipt")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()



