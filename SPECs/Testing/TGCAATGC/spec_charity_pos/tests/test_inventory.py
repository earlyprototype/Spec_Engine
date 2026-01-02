"""
Tests for Inventory Management
"""

import pytest
from decimal import Decimal
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import init_database, Item, Category
from inventory import InventoryManager


@pytest.fixture
def test_db():
    """Create test database"""
    db_manager = init_database(':memory:')  # In-memory database for testing
    yield db_manager
    # Cleanup handled by in-memory database


@pytest.fixture
def inventory_manager(test_db):
    """Create inventory manager with test database"""
    session = test_db.get_session()
    manager = InventoryManager(session)
    yield manager
    session.close()


def test_add_item(inventory_manager):
    """Test adding item to inventory"""
    item = inventory_manager.add_item(
        name="Test Book",
        price=Decimal('5.99'),
        stock_quantity=3
    )
    
    assert item.id is not None
    assert item.name == "Test Book"
    assert item.price == Decimal('5.99')
    assert item.stock_quantity == 3


def test_get_item(inventory_manager):
    """Test retrieving item by ID"""
    item = inventory_manager.add_item("Test Item", Decimal('10.00'))
    
    retrieved = inventory_manager.get_item(item.id)
    assert retrieved is not None
    assert retrieved.id == item.id
    assert retrieved.name == "Test Item"


def test_update_item(inventory_manager):
    """Test updating item"""
    item = inventory_manager.add_item("Original Name", Decimal('5.00'))
    
    updated = inventory_manager.update_item(
        item.id,
        name="Updated Name",
        price=Decimal('7.50')
    )
    
    assert updated.name == "Updated Name"
    assert updated.price == Decimal('7.50')


def test_delete_item(inventory_manager):
    """Test deleting item"""
    item = inventory_manager.add_item("To Delete", Decimal('1.00'))
    
    result = inventory_manager.delete_item(item.id)
    assert result is True
    
    retrieved = inventory_manager.get_item(item.id)
    assert retrieved is None


def test_search_items(inventory_manager):
    """Test item search"""
    inventory_manager.add_item("Python Book", Decimal('12.00'))
    inventory_manager.add_item("Java Book", Decimal('15.00'))
    inventory_manager.add_item("Python Mug", Decimal('5.00'))
    
    results = inventory_manager.search_items("Python")
    assert len(results) == 2


def test_add_category(inventory_manager):
    """Test adding category"""
    category = inventory_manager.add_category(
        name="Books",
        description="All books"
    )
    
    assert category.id is not None
    assert category.name == "Books"


def test_stock_management(inventory_manager):
    """Test stock updates"""
    item = inventory_manager.add_item("Test Item", Decimal('10.00'), stock_quantity=5)
    
    # Increase stock
    updated = inventory_manager.update_stock(item.id, 3)
    assert updated.stock_quantity == 8
    
    # Decrease stock
    updated = inventory_manager.update_stock(item.id, -2)
    assert updated.stock_quantity == 6


def test_low_stock_items(inventory_manager):
    """Test low stock detection"""
    inventory_manager.add_item("Low Stock", Decimal('5.00'), stock_quantity=2)
    inventory_manager.add_item("Good Stock", Decimal('5.00'), stock_quantity=10)
    
    low_stock = inventory_manager.get_low_stock_items(threshold=5)
    assert len(low_stock) == 1
    assert low_stock[0].name == "Low Stock"


def test_inventory_value(inventory_manager):
    """Test inventory value calculation"""
    inventory_manager.add_item("Item 1", Decimal('10.00'), stock_quantity=5)
    inventory_manager.add_item("Item 2", Decimal('20.00'), stock_quantity=3)
    
    value_info = inventory_manager.get_inventory_value()
    expected_value = (Decimal('10.00') * 5) + (Decimal('20.00') * 3)
    
    assert value_info['total_value'] == expected_value



