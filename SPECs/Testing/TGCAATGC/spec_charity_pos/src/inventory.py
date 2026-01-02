"""
Charity Shop POS - Inventory Management
Complete CRUD operations for items, categories, and stock management
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from database import Item, Category, Donation, get_session


class InventoryManager:
    """Handles all inventory management operations"""
    
    def __init__(self, session: Session = None):
        """
        Initialize inventory manager
        
        Args:
            session: SQLAlchemy session (creates new if not provided)
        """
        self.session = session or get_session()
        self._own_session = session is None
    
    def __del__(self):
        """Clean up session if we created it"""
        if self._own_session and self.session:
            self.session.close()
    
    # ===== ITEM CRUD OPERATIONS =====
    
    def add_item(self, name: str, price: Decimal, category_id: Optional[int] = None,
                 description: str = None, stock_quantity: int = 1,
                 sku: str = None, donation_id: int = None) -> Item:
        """
        Add new item to inventory
        
        Args:
            name: Item name
            price: Sale price
            category_id: Category ID (optional)
            description: Item description (optional)
            stock_quantity: Initial stock quantity
            sku: Stock keeping unit code (optional, must be unique)
            donation_id: Associated donation ID (optional)
        
        Returns:
            Created Item object
        """
        item = Item(
            name=name,
            price=price,
            category_id=category_id,
            description=description,
            stock_quantity=stock_quantity,
            sku=sku,
            donation_id=donation_id
        )
        
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        
        return item
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """
        Get item by ID
        
        Args:
            item_id: Item ID
        
        Returns:
            Item object or None if not found
        """
        return self.session.query(Item).filter(Item.id == item_id).first()
    
    def get_item_by_sku(self, sku: str) -> Optional[Item]:
        """
        Get item by SKU code
        
        Args:
            sku: Stock keeping unit code
        
        Returns:
            Item object or None if not found
        """
        return self.session.query(Item).filter(Item.sku == sku).first()
    
    def update_item(self, item_id: int, **kwargs) -> Optional[Item]:
        """
        Update item fields
        
        Args:
            item_id: Item ID
            **kwargs: Fields to update (name, price, description, etc.)
        
        Returns:
            Updated Item object or None if not found
        """
        item = self.get_item(item_id)
        if not item:
            return None
        
        # Update allowed fields
        allowed_fields = ['name', 'description', 'price', 'category_id', 
                         'stock_quantity', 'sku']
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(item, field, value)
        
        self.session.commit()
        self.session.refresh(item)
        
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """
        Delete item from inventory
        
        Args:
            item_id: Item ID
        
        Returns:
            True if deleted, False if not found
        """
        item = self.get_item(item_id)
        if not item:
            return False
        
        self.session.delete(item)
        self.session.commit()
        
        return True
    
    def search_items(self, query: str = None, category_id: int = None,
                     min_price: Decimal = None, max_price: Decimal = None,
                     in_stock_only: bool = False) -> List[Item]:
        """
        Search items with various filters
        
        Args:
            query: Search term for name/description
            category_id: Filter by category
            min_price: Minimum price
            max_price: Maximum price
            in_stock_only: Show only items in stock
        
        Returns:
            List of matching Item objects
        """
        filters = []
        
        # Text search in name and description
        if query:
            search_filter = or_(
                Item.name.ilike(f'%{query}%'),
                Item.description.ilike(f'%{query}%'),
                Item.sku.ilike(f'%{query}%')
            )
            filters.append(search_filter)
        
        # Category filter
        if category_id:
            filters.append(Item.category_id == category_id)
        
        # Price range
        if min_price is not None:
            filters.append(Item.price >= min_price)
        if max_price is not None:
            filters.append(Item.price <= max_price)
        
        # Stock filter
        if in_stock_only:
            filters.append(Item.stock_quantity > 0)
        
        # Build and execute query
        query_obj = self.session.query(Item)
        if filters:
            query_obj = query_obj.filter(and_(*filters))
        
        return query_obj.all()
    
    def list_all_items(self, limit: int = 100, offset: int = 0) -> List[Item]:
        """
        List all items with pagination
        
        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
        
        Returns:
            List of Item objects
        """
        return self.session.query(Item).limit(limit).offset(offset).all()
    
    # ===== CATEGORY MANAGEMENT =====
    
    def add_category(self, name: str, description: str = None,
                     parent_id: int = None) -> Category:
        """
        Add new category
        
        Args:
            name: Category name
            description: Category description (optional)
            parent_id: Parent category ID for hierarchy (optional)
        
        Returns:
            Created Category object
        """
        category = Category(
            name=name,
            description=description,
            parent_id=parent_id
        )
        
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        
        return category
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.session.query(Category).filter(Category.id == category_id).first()
    
    def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        """Update category fields"""
        category = self.get_category(category_id)
        if not category:
            return None
        
        allowed_fields = ['name', 'description', 'parent_id']
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(category, field, value)
        
        self.session.commit()
        self.session.refresh(category)
        
        return category
    
    def delete_category(self, category_id: int, reassign_to: int = None) -> bool:
        """
        Delete category
        
        Args:
            category_id: Category ID to delete
            reassign_to: Category ID to reassign items to (optional)
        
        Returns:
            True if deleted, False if not found
        """
        category = self.get_category(category_id)
        if not category:
            return False
        
        # Reassign items if needed
        if reassign_to:
            items = self.session.query(Item).filter(Item.category_id == category_id).all()
            for item in items:
                item.category_id = reassign_to
            self.session.commit()
        
        self.session.delete(category)
        self.session.commit()
        
        return True
    
    def list_all_categories(self) -> List[Category]:
        """List all categories"""
        return self.session.query(Category).all()
    
    def get_category_tree(self) -> List[Dict[str, Any]]:
        """
        Get hierarchical category tree
        
        Returns:
            List of category dicts with nested subcategories
        """
        def build_tree(parent_id=None):
            categories = self.session.query(Category).filter(
                Category.parent_id == parent_id
            ).all()
            
            result = []
            for cat in categories:
                cat_dict = {
                    'id': cat.id,
                    'name': cat.name,
                    'description': cat.description,
                    'subcategories': build_tree(cat.id)
                }
                result.append(cat_dict)
            
            return result
        
        return build_tree()
    
    # ===== STOCK MANAGEMENT =====
    
    def update_stock(self, item_id: int, quantity_change: int) -> Optional[Item]:
        """
        Update item stock quantity
        
        Args:
            item_id: Item ID
            quantity_change: Change in quantity (positive to add, negative to remove)
        
        Returns:
            Updated Item object or None if not found
        """
        item = self.get_item(item_id)
        if not item:
            return None
        
        item.stock_quantity += quantity_change
        
        # Don't allow negative stock
        if item.stock_quantity < 0:
            item.stock_quantity = 0
        
        self.session.commit()
        self.session.refresh(item)
        
        return item
    
    def set_stock(self, item_id: int, quantity: int) -> Optional[Item]:
        """
        Set absolute stock quantity
        
        Args:
            item_id: Item ID
            quantity: New stock quantity
        
        Returns:
            Updated Item object or None if not found
        """
        return self.update_item(item_id, stock_quantity=quantity)
    
    def get_low_stock_items(self, threshold: int = 5) -> List[Item]:
        """
        Get items with stock below threshold
        
        Args:
            threshold: Stock level threshold
        
        Returns:
            List of Item objects with low stock
        """
        return self.session.query(Item).filter(
            Item.stock_quantity <= threshold,
            Item.stock_quantity > 0
        ).all()
    
    def get_out_of_stock_items(self) -> List[Item]:
        """Get items that are out of stock"""
        return self.session.query(Item).filter(Item.stock_quantity == 0).all()
    
    # ===== DONATION TRACKING =====
    
    def add_donation(self, donor_name: str = None, donor_contact: str = None,
                     total_value: Decimal = None, notes: str = None) -> Donation:
        """
        Record a new donation
        
        Args:
            donor_name: Name of donor (optional)
            donor_contact: Contact information (optional)
            total_value: Estimated value (optional)
            notes: Additional notes (optional)
        
        Returns:
            Created Donation object
        """
        donation = Donation(
            donor_name=donor_name,
            donor_contact=donor_contact,
            total_value=total_value,
            notes=notes
        )
        
        self.session.add(donation)
        self.session.commit()
        self.session.refresh(donation)
        
        return donation
    
    def get_donation(self, donation_id: int) -> Optional[Donation]:
        """Get donation by ID"""
        return self.session.query(Donation).filter(Donation.id == donation_id).first()
    
    def update_donation(self, donation_id: int, **kwargs) -> Optional[Donation]:
        """Update donation fields"""
        donation = self.get_donation(donation_id)
        if not donation:
            return None
        
        allowed_fields = ['donor_name', 'donor_contact', 'total_value', 'notes']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(donation, field, value)
        
        self.session.commit()
        self.session.refresh(donation)
        
        return donation
    
    def list_donations(self, limit: int = 100) -> List[Donation]:
        """List recent donations"""
        return self.session.query(Donation).order_by(
            Donation.donation_date.desc()
        ).limit(limit).all()
    
    def get_items_from_donation(self, donation_id: int) -> List[Item]:
        """Get all items from a specific donation"""
        return self.session.query(Item).filter(Item.donation_id == donation_id).all()
    
    # ===== UTILITY FUNCTIONS =====
    
    def get_inventory_value(self) -> Dict[str, Decimal]:
        """
        Calculate total inventory value
        
        Returns:
            Dict with total_value and in_stock_value
        """
        items = self.list_all_items()
        
        total_value = sum(item.price * item.stock_quantity for item in items)
        in_stock_value = sum(
            item.price * item.stock_quantity 
            for item in items 
            if item.stock_quantity > 0
        )
        
        return {
            'total_value': Decimal(str(total_value)),
            'in_stock_value': Decimal(str(in_stock_value)),
            'total_items': len(items),
            'in_stock_items': sum(1 for item in items if item.stock_quantity > 0)
        }
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get comprehensive inventory summary"""
        value_info = self.get_inventory_value()
        low_stock = self.get_low_stock_items()
        out_of_stock = self.get_out_of_stock_items()
        
        return {
            **value_info,
            'low_stock_count': len(low_stock),
            'out_of_stock_count': len(out_of_stock),
            'categories_count': len(self.list_all_categories())
        }


# Convenience functions

def quick_add_item(name: str, price: float, **kwargs) -> Item:
    """Quick add item with automatic session management"""
    manager = InventoryManager()
    item = manager.add_item(name, Decimal(str(price)), **kwargs)
    return item


def quick_search(query: str) -> List[Item]:
    """Quick search with automatic session management"""
    manager = InventoryManager()
    return manager.search_items(query)


if __name__ == '__main__':
    # Test inventory operations
    print("Testing Inventory Management...")
    
    manager = InventoryManager()
    
    # Test add item
    print("\n1. Adding test item...")
    item = manager.add_item(
        name="Test Book",
        price=Decimal('5.99'),
        description="A test book item",
        stock_quantity=3
    )
    print(f"   Created: {item}")
    
    # Test search
    print("\n2. Searching for 'test'...")
    results = manager.search_items('test')
    print(f"   Found {len(results)} item(s)")
    
    # Test update
    print("\n3. Updating item...")
    updated = manager.update_item(item.id, price=Decimal('4.99'))
    print(f"   Updated: {updated}")
    
    # Test inventory summary
    print("\n4. Inventory summary...")
    summary = manager.get_inventory_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n✓ Inventory management test completed!")



