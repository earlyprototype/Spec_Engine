"""
Tests for Payment Processing
"""

import pytest
from decimal import Decimal
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from payment_processor import (
    CashPaymentProcessor, CardPaymentProcessor, PaymentManager, PaymentMethod
)


def test_cash_payment_success():
    """Test successful cash payment"""
    processor = CashPaymentProcessor()
    result = processor.process_payment(Decimal('10.00'), Decimal('20.00'))
    
    assert result.success is True
    assert result.payment_data['change'] == 10.0


def test_cash_payment_insufficient():
    """Test insufficient cash payment"""
    processor = CashPaymentProcessor()
    result = processor.process_payment(Decimal('20.00'), Decimal('10.00'))
    
    assert result.success is False
    assert 'Insufficient' in result.message


def test_change_calculation():
    """Test change calculation"""
    processor = CashPaymentProcessor()
    change = processor.calculate_change(Decimal('15.50'), Decimal('20.00'))
    
    assert change == Decimal('4.50')


def test_change_breakdown():
    """Test change denomination breakdown"""
    processor = CashPaymentProcessor()
    breakdown = processor.suggest_change_breakdown(Decimal('4.50'))
    
    assert '£2' in breakdown
    assert '£1' in breakdown or '£2' in breakdown
    assert '50p' in breakdown or '20p' in breakdown


def test_card_payment_test_mode():
    """Test card payment in test mode"""
    processor = CardPaymentProcessor(test_mode=True)
    result = processor.process_payment(Decimal('25.99'), card_token='test_1234')
    
    assert result.success is True
    assert result.transaction_id is not None
    assert result.payment_data['test_mode'] is True


def test_payment_manager_cash():
    """Test payment manager with cash"""
    manager = PaymentManager()
    result = manager.process_payment(
        PaymentMethod.CASH,
        Decimal('15.00'),
        cash_given=Decimal('20.00')
    )
    
    assert result.success is True


def test_payment_manager_card():
    """Test payment manager with card"""
    manager = PaymentManager()
    result = manager.process_payment(
        PaymentMethod.CARD,
        Decimal('25.00'),
        card_token='test_card'
    )
    
    assert result.success is True



