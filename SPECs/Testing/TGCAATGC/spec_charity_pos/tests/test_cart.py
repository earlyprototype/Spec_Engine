"""
Tests for Shopping Cart
"""

import pytest
from decimal import Decimal
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cart import ShoppingCart, CartItem


def test_cart_initialization():
    """Test cart initialization"""
    cart = ShoppingCart()
    assert cart.is_empty() is True
    assert cart.get_total() == Decimal('0.00')


def test_add_item():
    """Test adding item to cart"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    
    assert cart.is_empty() is False
    assert cart.get_unique_item_count() == 1
    assert cart.get_item_count() == 1


def test_add_multiple_quantities():
    """Test adding multiple quantities"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    
    assert cart.get_item_count() == 2
    assert cart.get_total() == Decimal('11.98')


def test_add_existing_item():
    """Test adding item that already exists in cart"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    
    assert cart.get_unique_item_count() == 1
    assert cart.get_item_count() == 3


def test_remove_item():
    """Test removing item from cart"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    cart.remove_item(1)
    
    assert cart.is_empty() is True


def test_update_quantity():
    """Test updating item quantity"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    cart.update_quantity(1, 3)
    
    assert cart.get_item_count() == 3


def test_update_quantity_to_zero():
    """Test updating quantity to zero removes item"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    cart.update_quantity(1, 0)
    
    assert cart.is_empty() is True


def test_cart_total():
    """Test cart total calculation"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    cart.add_item(2, "Mug", Decimal('3.50'), 1)
    
    expected = (Decimal('5.99') * 2) + Decimal('3.50')
    assert cart.get_total() == expected


def test_clear_cart():
    """Test clearing cart"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    cart.add_item(2, "Mug", Decimal('3.50'), 1)
    cart.clear()
    
    assert cart.is_empty() is True
    assert cart.get_total() == Decimal('0.00')


def test_cart_to_dict():
    """Test converting cart to dictionary"""
    cart = ShoppingCart()
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    
    cart_dict = cart.to_dict()
    assert 'items' in cart_dict
    assert 'total' in cart_dict
    assert len(cart_dict['items']) == 1



