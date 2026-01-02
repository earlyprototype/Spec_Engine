"""
Charity Shop POS - Shopping Cart
Manages items in cart before transaction completion
"""

from decimal import Decimal
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class CartItem:
    """Represents an item in the shopping cart"""
    item_id: int
    name: str
    unit_price: Decimal
    quantity: int = 1
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item"""
        return self.unit_price * self.quantity
    
    def __repr__(self):
        return f"CartItem({self.name} x{self.quantity} @ £{self.unit_price} = £{self.subtotal})"


class ShoppingCart:
    """Shopping cart for building transactions"""
    
    def __init__(self):
        """Initialize empty shopping cart"""
        self._items: Dict[int, CartItem] = {}
    
    def add_item(self, item_id: int, name: str, price: Decimal, quantity: int = 1) -> CartItem:
        """
        Add item to cart or update quantity if already exists
        
        Args:
            item_id: Database item ID
            name: Item name
            price: Unit price
            quantity: Quantity to add (default: 1)
        
        Returns:
            CartItem that was added/updated
        """
        if item_id in self._items:
            # Item already in cart, increase quantity
            self._items[item_id].quantity += quantity
        else:
            # New item
            self._items[item_id] = CartItem(
                item_id=item_id,
                name=name,
                unit_price=price,
                quantity=quantity
            )
        
        return self._items[item_id]
    
    def remove_item(self, item_id: int) -> bool:
        """
        Remove item completely from cart
        
        Args:
            item_id: Item ID to remove
        
        Returns:
            True if removed, False if not in cart
        """
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
    
    def update_quantity(self, item_id: int, quantity: int) -> Optional[CartItem]:
        """
        Update quantity for an item
        
        Args:
            item_id: Item ID
            quantity: New quantity (0 removes item)
        
        Returns:
            Updated CartItem or None if not in cart
        """
        if item_id not in self._items:
            return None
        
        if quantity <= 0:
            self.remove_item(item_id)
            return None
        
        self._items[item_id].quantity = quantity
        return self._items[item_id]
    
    def get_item(self, item_id: int) -> Optional[CartItem]:
        """Get cart item by ID"""
        return self._items.get(item_id)
    
    def get_all_items(self) -> List[CartItem]:
        """Get list of all items in cart"""
        return list(self._items.values())
    
    def get_total(self) -> Decimal:
        """Calculate total cart value"""
        return sum(item.subtotal for item in self._items.values())
    
    def get_item_count(self) -> int:
        """Get total number of items in cart (sum of quantities)"""
        return sum(item.quantity for item in self._items.values())
    
    def get_unique_item_count(self) -> int:
        """Get number of unique items in cart"""
        return len(self._items)
    
    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self._items) == 0
    
    def clear(self):
        """Remove all items from cart"""
        self._items.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert cart to dictionary representation
        
        Returns:
            Dict with cart summary and items
        """
        return {
            'items': [
                {
                    'item_id': item.item_id,
                    'name': item.name,
                    'unit_price': float(item.unit_price),
                    'quantity': item.quantity,
                    'subtotal': float(item.subtotal)
                }
                for item in self._items.values()
            ],
            'total': float(self.get_total()),
            'item_count': self.get_item_count(),
            'unique_items': self.get_unique_item_count()
        }
    
    def __repr__(self):
        return f"ShoppingCart({self.get_unique_item_count()} items, total=£{self.get_total()})"
    
    def __str__(self):
        """Human-readable cart summary"""
        if self.is_empty():
            return "Shopping Cart: Empty"
        
        lines = ["Shopping Cart:"]
        for item in self._items.values():
            lines.append(f"  {item.name} x{item.quantity} @ £{item.unit_price} = £{item.subtotal}")
        lines.append(f"\nTotal: £{self.get_total()}")
        
        return "\n".join(lines)


if __name__ == '__main__':
    # Test shopping cart
    print("Testing Shopping Cart...")
    
    cart = ShoppingCart()
    
    # Add items
    print("\n1. Adding items...")
    cart.add_item(1, "Book", Decimal('5.99'), 2)
    cart.add_item(2, "Mug", Decimal('3.50'), 1)
    cart.add_item(3, "T-Shirt", Decimal('8.00'), 1)
    print(cart)
    
    # Add more of existing item
    print("\n2. Adding more books...")
    cart.add_item(1, "Book", Decimal('5.99'), 1)
    print(cart)
    
    # Update quantity
    print("\n3. Updating T-Shirt quantity to 2...")
    cart.update_quantity(3, 2)
    print(cart)
    
    # Remove item
    print("\n4. Removing Mug...")
    cart.remove_item(2)
    print(cart)
    
    # Get total
    print(f"\n5. Cart total: £{cart.get_total()}")
    print(f"   Item count: {cart.get_item_count()}")
    print(f"   Unique items: {cart.get_unique_item_count()}")
    
    # Clear cart
    print("\n6. Clearing cart...")
    cart.clear()
    print(cart)
    
    print("\n✓ Shopping cart test completed!")



