"""
Charity Shop POS - Database Models
SQLAlchemy ORM models for all system entities
"""

from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, Date,
    ForeignKey, DECIMAL, Boolean, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """Staff and volunteer user accounts"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # 'admin' or 'volunteer'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = relationship('Transaction', back_populates='user')
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


class Category(Base):
    """Hierarchical item categories"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    parent = relationship('Category', remote_side=[id], backref='subcategories')
    items = relationship('Item', back_populates='category')
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"


class Donation(Base):
    """Donation records from donors"""
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    donor_name = Column(String(100), nullable=True)
    donor_contact = Column(String(100), nullable=True)
    donation_date = Column(Date, default=date.today)
    total_value = Column(DECIMAL(10, 2), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    items = relationship('Item', back_populates='donation')
    
    # Index
    __table_args__ = (
        Index('idx_donations_date', 'donation_date'),
    )
    
    def __repr__(self):
        return f"<Donation(donor='{self.donor_name}', date='{self.donation_date}')>"


class Item(Base):
    """Inventory items available for sale"""
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    stock_quantity = Column(Integer, default=1)
    sku = Column(String(50), unique=True, nullable=True)
    donation_id = Column(Integer, ForeignKey('donations.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship('Category', back_populates='items')
    donation = relationship('Donation', back_populates='items')
    transaction_items = relationship('TransactionItem', back_populates='item')
    
    # Indexes
    __table_args__ = (
        Index('idx_items_category', 'category_id'),
        Index('idx_items_sku', 'sku'),
    )
    
    def __repr__(self):
        return f"<Item(name='{self.name}', price={self.price}, stock={self.stock_quantity})>"
    
    def is_in_stock(self):
        """Check if item is available for sale"""
        return self.stock_quantity > 0
    
    def is_low_stock(self, threshold=5):
        """Check if stock is below threshold"""
        return self.stock_quantity <= threshold


class Transaction(Base):
    """Sales transaction records"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_method = Column(String(20), nullable=False)  # 'cash', 'card', 'other'
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    cash_given = Column(DECIMAL(10, 2), nullable=True)
    change_returned = Column(DECIMAL(10, 2), nullable=True)
    status = Column(String(20), default='completed')  # 'completed', 'cancelled', 'refunded'
    
    # Relationships
    user = relationship('User', back_populates='transactions')
    transaction_items = relationship('TransactionItem', back_populates='transaction', cascade='all, delete-orphan')
    receipt = relationship('Receipt', back_populates='transaction', uselist=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_transactions_user', 'user_id'),
        Index('idx_transactions_timestamp', 'timestamp'),
        Index('idx_transactions_status', 'status'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, total={self.total_amount}, status='{self.status}')>"
    
    def calculate_total(self):
        """Calculate total from transaction items"""
        return sum(item.subtotal for item in self.transaction_items)
    
    def calculate_change(self):
        """Calculate change for cash transactions"""
        if self.payment_method == 'cash' and self.cash_given:
            return self.cash_given - self.total_amount
        return Decimal('0.00')


class TransactionItem(Base):
    """Line items in transactions (many-to-many link)"""
    __tablename__ = 'transaction_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    transaction = relationship('Transaction', back_populates='transaction_items')
    item = relationship('Item', back_populates='transaction_items')
    
    # Indexes
    __table_args__ = (
        Index('idx_transaction_items_transaction', 'transaction_id'),
        Index('idx_transaction_items_item', 'item_id'),
    )
    
    def __repr__(self):
        return f"<TransactionItem(item_id={self.item_id}, qty={self.quantity}, subtotal={self.subtotal})>"
    
    def calculate_subtotal(self):
        """Calculate subtotal from quantity and unit price"""
        return self.quantity * self.unit_price


class Receipt(Base):
    """Generated receipts for transactions"""
    __tablename__ = 'receipts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), unique=True, nullable=False)
    receipt_number = Column(String(50), unique=True, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    format = Column(String(10), nullable=False)  # 'html', 'pdf', 'text'
    file_path = Column(String(255), nullable=True)
    
    # Relationships
    transaction = relationship('Transaction', back_populates='receipt')
    
    # Index
    __table_args__ = (
        Index('idx_receipts_transaction', 'transaction_id'),
    )
    
    def __repr__(self):
        return f"<Receipt(number='{self.receipt_number}', format='{self.format}')>"


class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, db_path='transactions.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all tables from models"""
        Base.metadata.create_all(self.engine)
        
    def drop_tables(self):
        """Drop all tables (use with caution)"""
        Base.metadata.drop_all(self.engine)
        
    def get_session(self):
        """Get new database session"""
        return self.Session()
    
    def backup_database(self, backup_path):
        """Create backup of database file"""
        import shutil
        from pathlib import Path
        
        if Path(self.db_path).exists():
            shutil.copy2(self.db_path, backup_path)
            return True
        return False


# Convenience functions

def init_database(db_path='transactions.db'):
    """Initialize database with all tables"""
    db_manager = DatabaseManager(db_path)
    db_manager.create_tables()
    return db_manager


def get_session(db_path='transactions.db'):
    """Get database session (convenience function)"""
    db_manager = DatabaseManager(db_path)
    return db_manager.get_session()


if __name__ == '__main__':
    # Test database creation
    print("Creating database schema...")
    db_manager = init_database('test_charity_pos.db')
    print("Database schema created successfully!")
    
    # Create test session
    session = db_manager.get_session()
    
    # Test data
    print("\nCreating test data...")
    admin = User(username='admin', password_hash='hashed_password', role='admin')
    category = Category(name='Books', description='All book items')
    session.add_all([admin, category])
    session.commit()
    
    print(f"Created: {admin}")
    print(f"Created: {category}")
    
    session.close()
    print("\nDatabase test completed successfully!")



