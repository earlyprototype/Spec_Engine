"""
Charity Shop POS - Authentication and Authorization
User login and role-based permissions
"""

import hashlib
from typing import Optional
from sqlalchemy.orm import Session

from database import User, get_session


class AuthManager:
    """Manages user authentication and authorization"""
    
    def __init__(self, session: Session = None):
        """
        Initialize authentication manager
        
        Args:
            session: SQLAlchemy session (creates new if not provided)
        """
        self.session = session or get_session()
        self._own_session = session is None
    
    def __del__(self):
        """Clean up session if we created it"""
        if self._own_session and self.session:
            self.session.close()
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA256
        (In production, use bcrypt or similar)
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            User object if authenticated, None otherwise
        """
        user = self.session.query(User).filter(User.username == username).first()
        
        if not user:
            return None
        
        password_hash = self.hash_password(password)
        
        if user.password_hash == password_hash:
            return user
        
        return None
    
    def create_user(self, username: str, password: str, role: str = 'volunteer') -> User:
        """
        Create new user
        
        Args:
            username: Username (must be unique)
            password: Plain text password
            role: User role ('admin' or 'volunteer')
        
        Returns:
            Created User object
        """
        if role not in ['admin', 'volunteer']:
            raise ValueError("Role must be 'admin' or 'volunteer'")
        
        # Check if username already exists
        existing = self.session.query(User).filter(User.username == username).first()
        if existing:
            raise ValueError(f"Username '{username}' already exists")
        
        user = User(
            username=username,
            password_hash=self.hash_password(password),
            role=role
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            username: Username
            old_password: Current password
            new_password: New password
        
        Returns:
            True if changed successfully, False otherwise
        """
        user = self.authenticate(username, old_password)
        if not user:
            return False
        
        user.password_hash = self.hash_password(new_password)
        self.session.commit()
        
        return True
    
    def has_permission(self, user: User, permission: str) -> bool:
        """
        Check if user has specific permission
        
        Args:
            user: User object
            permission: Permission to check
        
        Returns:
            True if user has permission
        """
        # Admin has all permissions
        if user.role == 'admin':
            return True
        
        # Volunteer permissions
        volunteer_permissions = [
            'process_sale',
            'view_inventory',
            'record_donation',
            'generate_receipt'
        ]
        
        if user.role == 'volunteer':
            return permission in volunteer_permissions
        
        return False


if __name__ == '__main__':
    # Test authentication
    print("Testing Authentication...")
    
    auth_manager = AuthManager()
    
    # Create test user
    print("\n1. Creating test user...")
    try:
        user = auth_manager.create_user('testuser', 'password123', 'volunteer')
        print(f"   Created: {user}")
    except ValueError as e:
        print(f"   {e}")
    
    # Authenticate
    print("\n2. Testing authentication...")
    user = auth_manager.authenticate('testuser', 'password123')
    if user:
        print(f"   ✓ Authenticated: {user.username} ({user.role})")
    else:
        print("   ✗ Authentication failed")
    
    # Wrong password
    print("\n3. Testing wrong password...")
    user = auth_manager.authenticate('testuser', 'wrongpassword')
    if user:
        print("   ✗ Should have failed!")
    else:
        print("   ✓ Correctly rejected")
    
    # Check permissions
    print("\n4. Testing permissions...")
    user = auth_manager.authenticate('testuser', 'password123')
    if user:
        print(f"   process_sale: {auth_manager.has_permission(user, 'process_sale')}")
        print(f"   manage_users: {auth_manager.has_permission(user, 'manage_users')}")
    
    print("\n✓ Authentication test completed!")



