"""
Charity Shop POS - Payment Processing
Handles cash and card payment processing
"""

from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class PaymentMethod(Enum):
    """Payment method types"""
    CASH = "cash"
    CARD = "card"
    OTHER = "other"


class PaymentResult:
    """Result of a payment processing attempt"""
    
    def __init__(self, success: bool, message: str = "",
                 transaction_id: str = None, payment_data: Dict[str, Any] = None):
        """
        Initialize payment result
        
        Args:
            success: Whether payment succeeded
            message: Result message or error description
            transaction_id: External transaction ID (for card payments)
            payment_data: Additional payment data
        """
        self.success = success
        self.message = message
        self.transaction_id = transaction_id
        self.payment_data = payment_data or {}
        self.timestamp = datetime.utcnow()
    
    def __repr__(self):
        return f"PaymentResult(success={self.success}, message='{self.message}')"


class CashPaymentProcessor:
    """Processes cash payments"""
    
    def process_payment(self, amount: Decimal, cash_given: Decimal) -> PaymentResult:
        """
        Process cash payment
        
        Args:
            amount: Required payment amount
            cash_given: Amount of cash provided by customer
        
        Returns:
            PaymentResult object
        """
        # Validate amounts
        if amount <= 0:
            return PaymentResult(
                success=False,
                message="Invalid payment amount"
            )
        
        if cash_given < amount:
            return PaymentResult(
                success=False,
                message=f"Insufficient cash. Required: £{amount}, Given: £{cash_given}"
            )
        
        # Calculate change
        change = cash_given - amount
        
        return PaymentResult(
            success=True,
            message="Cash payment successful",
            payment_data={
                'amount': float(amount),
                'cash_given': float(cash_given),
                'change': float(change),
                'payment_method': 'cash'
            }
        )
    
    def calculate_change(self, amount: Decimal, cash_given: Decimal) -> Decimal:
        """Calculate change to return"""
        return max(cash_given - amount, Decimal('0.00'))
    
    def suggest_change_breakdown(self, change: Decimal) -> Dict[str, int]:
        """
        Suggest denominations for giving change
        
        Args:
            change: Amount of change to give
        
        Returns:
            Dict of denomination -> count
        """
        # UK denominations in pence
        denominations = [
            ('£50', 5000),
            ('£20', 2000),
            ('£10', 1000),
            ('£5', 500),
            ('£2', 200),
            ('£1', 100),
            ('50p', 50),
            ('20p', 20),
            ('10p', 10),
            ('5p', 5),
            ('2p', 2),
            ('1p', 1),
        ]
        
        change_pence = int(change * 100)
        breakdown = {}
        
        for name, value in denominations:
            if change_pence >= value:
                count = change_pence // value
                breakdown[name] = count
                change_pence -= count * value
        
        return breakdown


class CardPaymentProcessor:
    """Processes card payments (stub for Square/Stripe integration)"""
    
    def __init__(self, api_key: str = None, test_mode: bool = True):
        """
        Initialize card payment processor
        
        Args:
            api_key: Payment processor API key
            test_mode: Use test mode (default: True)
        """
        self.api_key = api_key
        self.test_mode = test_mode
        self._initialized = api_key is not None
    
    def process_payment(self, amount: Decimal, card_token: str = None,
                       card_details: Dict[str, Any] = None) -> PaymentResult:
        """
        Process card payment
        
        Args:
            amount: Payment amount
            card_token: Tokenized card information
            card_details: Manual card entry details (fallback)
        
        Returns:
            PaymentResult object
        """
        # Validate amount
        if amount <= 0:
            return PaymentResult(
                success=False,
                message="Invalid payment amount"
            )
        
        # In test mode or if not initialized, simulate payment
        if self.test_mode or not self._initialized:
            return self._simulate_payment(amount, card_token)
        
        # Real payment processing would go here
        # For now, return not implemented
        return PaymentResult(
            success=False,
            message="Card payment integration not configured. Use test mode or configure API key."
        )
    
    def _simulate_payment(self, amount: Decimal, card_token: str = None) -> PaymentResult:
        """
        Simulate card payment for testing
        
        Args:
            amount: Payment amount
            card_token: Optional card token
        
        Returns:
            PaymentResult object (always successful in simulation)
        """
        transaction_id = f"TEST_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        return PaymentResult(
            success=True,
            message="Card payment successful (TEST MODE)",
            transaction_id=transaction_id,
            payment_data={
                'amount': float(amount),
                'payment_method': 'card',
                'test_mode': True,
                'card_last4': '****' + (card_token[-4:] if card_token else '0000')
            }
        )


class PaymentManager:
    """Unified payment management interface"""
    
    def __init__(self, card_api_key: str = None):
        """
        Initialize payment manager
        
        Args:
            card_api_key: API key for card payment processor
        """
        self.cash_processor = CashPaymentProcessor()
        self.card_processor = CardPaymentProcessor(card_api_key, test_mode=True)
    
    def process_payment(self, payment_method: PaymentMethod, amount: Decimal,
                       **kwargs) -> PaymentResult:
        """
        Process payment using specified method
        
        Args:
            payment_method: PaymentMethod enum value
            amount: Payment amount
            **kwargs: Additional payment-specific parameters
        
        Returns:
            PaymentResult object
        """
        if payment_method == PaymentMethod.CASH:
            cash_given = kwargs.get('cash_given')
            if cash_given is None:
                return PaymentResult(
                    success=False,
                    message="Cash amount not provided"
                )
            return self.cash_processor.process_payment(amount, cash_given)
        
        elif payment_method == PaymentMethod.CARD:
            card_token = kwargs.get('card_token')
            card_details = kwargs.get('card_details')
            return self.card_processor.process_payment(amount, card_token, card_details)
        
        else:
            return PaymentResult(
                success=False,
                message=f"Unsupported payment method: {payment_method}"
            )
    
    def calculate_cash_change(self, amount: Decimal, cash_given: Decimal) -> Decimal:
        """Calculate change for cash payment"""
        return self.cash_processor.calculate_change(amount, cash_given)
    
    def get_change_breakdown(self, change: Decimal) -> Dict[str, int]:
        """Get suggested change denominations"""
        return self.cash_processor.suggest_change_breakdown(change)


if __name__ == '__main__':
    # Test payment processing
    print("Testing Payment Processing...")
    
    manager = PaymentManager()
    
    # Test cash payment
    print("\n1. Cash payment test...")
    result = manager.process_payment(
        PaymentMethod.CASH,
        Decimal('15.50'),
        cash_given=Decimal('20.00')
    )
    print(f"   Result: {result}")
    print(f"   Data: {result.payment_data}")
    
    # Test change calculation
    print("\n2. Change breakdown...")
    change = Decimal('4.50')
    breakdown = manager.get_change_breakdown(change)
    print(f"   Change: £{change}")
    print(f"   Breakdown: {breakdown}")
    
    # Test card payment (test mode)
    print("\n3. Card payment test (test mode)...")
    result = manager.process_payment(
        PaymentMethod.CARD,
        Decimal('25.99'),
        card_token='test_card_1234'
    )
    print(f"   Result: {result}")
    print(f"   Transaction ID: {result.transaction_id}")
    print(f"   Data: {result.payment_data}")
    
    # Test insufficient cash
    print("\n4. Insufficient cash test...")
    result = manager.process_payment(
        PaymentMethod.CASH,
        Decimal('30.00'),
        cash_given=Decimal('20.00')
    )
    print(f"   Result: {result}")
    
    print("\n✓ Payment processing test completed!")



