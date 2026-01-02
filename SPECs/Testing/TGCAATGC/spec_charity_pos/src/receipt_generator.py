"""
Charity Shop POS - Receipt Generation
Generates formatted receipts in HTML, PDF, and text formats
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class ReceiptData:
    """Container for receipt information"""
    
    def __init__(self, transaction_id: int, items: List[Dict[str, Any]],
                 total: Decimal, payment_method: str,
                 cash_given: Decimal = None, change: Decimal = None,
                 timestamp: datetime = None, receipt_number: str = None,
                 cashier: str = None):
        """
        Initialize receipt data
        
        Args:
            transaction_id: Transaction ID
            items: List of items with name, quantity, price, subtotal
            total: Total amount
            payment_method: Payment method used
            cash_given: Cash amount given (for cash payments)
            change: Change returned (for cash payments)
            timestamp: Transaction timestamp
            receipt_number: Receipt number
            cashier: Cashier name
        """
        self.transaction_id = transaction_id
        self.items = items
        self.total = total
        self.payment_method = payment_method
        self.cash_given = cash_given
        self.change = change
        self.timestamp = timestamp or datetime.now()
        self.receipt_number = receipt_number or f"RCP-{transaction_id:06d}"
        self.cashier = cashier or "Staff"


class ReceiptGenerator:
    """Generates receipts in various formats"""
    
    def __init__(self, shop_name: str = "Charity Shop",
                 shop_address: str = None,
                 shop_phone: str = None,
                 charity_number: str = None):
        """
        Initialize receipt generator
        
        Args:
            shop_name: Name of shop
            shop_address: Shop address
            shop_phone: Shop phone number
            charity_number: Registered charity number
        """
        self.shop_name = shop_name
        self.shop_address = shop_address or "123 High Street, Town, AB12 3CD"
        self.shop_phone = shop_phone or "01234 567890"
        self.charity_number = charity_number or "123456"
    
    def generate_text_receipt(self, receipt_data: ReceiptData) -> str:
        """
        Generate plain text receipt
        
        Args:
            receipt_data: ReceiptData object
        
        Returns:
            Plain text receipt string
        """
        lines = []
        lines.append("=" * 50)
        lines.append(self.shop_name.center(50))
        lines.append(self.shop_address.center(50))
        lines.append(f"Tel: {self.shop_phone}".center(50))
        lines.append(f"Charity No: {self.charity_number}".center(50))
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Receipt: {receipt_data.receipt_number}")
        lines.append(f"Date: {receipt_data.timestamp.strftime('%d/%m/%Y %H:%M')}")
        lines.append(f"Cashier: {receipt_data.cashier}")
        lines.append("")
        lines.append("-" * 50)
        
        # Items
        for item in receipt_data.items:
            name = item['name'][:30]  # Truncate long names
            qty = item['quantity']
            price = item['unit_price']
            subtotal = item['subtotal']
            
            lines.append(f"{name:<30} {qty:>3} x £{price:>6.2f}  £{subtotal:>7.2f}")
        
        lines.append("-" * 50)
        lines.append(f"{'TOTAL':<44} £{receipt_data.total:>7.2f}")
        lines.append("")
        
        # Payment details
        lines.append(f"Payment Method: {receipt_data.payment_method.upper()}")
        if receipt_data.payment_method.lower() == 'cash':
            if receipt_data.cash_given:
                lines.append(f"Cash Given:     £{receipt_data.cash_given:>7.2f}")
            if receipt_data.change:
                lines.append(f"Change:         £{receipt_data.change:>7.2f}")
        
        lines.append("")
        lines.append("=" * 50)
        lines.append("Thank you for supporting our charity!".center(50))
        lines.append("Your purchase helps make a difference.".center(50))
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def generate_html_receipt(self, receipt_data: ReceiptData) -> str:
        """
        Generate HTML receipt
        
        Args:
            receipt_data: ReceiptData object
        
        Returns:
            HTML receipt string
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Receipt {receipt_data.receipt_number}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            max-width: 400px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ccc;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }}
        .shop-name {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .info {{
            font-size: 12px;
            margin-bottom: 20px;
        }}
        .items {{
            margin: 20px 0;
        }}
        .item-row {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            font-size: 14px;
        }}
        .item-name {{
            flex: 1;
        }}
        .item-qty {{
            width: 40px;
            text-align: center;
        }}
        .item-price {{
            width: 80px;
            text-align: right;
        }}
        .divider {{
            border-top: 1px dashed #000;
            margin: 10px 0;
        }}
        .total {{
            font-size: 18px;
            font-weight: bold;
            text-align: right;
            margin: 15px 0;
        }}
        .payment {{
            margin: 15px 0;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 2px solid #000;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="shop-name">{self.shop_name}</div>
        <div>{self.shop_address}</div>
        <div>Tel: {self.shop_phone}</div>
        <div>Charity No: {self.charity_number}</div>
    </div>
    
    <div class="info">
        <div>Receipt: {receipt_data.receipt_number}</div>
        <div>Date: {receipt_data.timestamp.strftime('%d/%m/%Y %H:%M')}</div>
        <div>Cashier: {receipt_data.cashier}</div>
    </div>
    
    <div class="divider"></div>
    
    <div class="items">
"""
        
        # Add items
        for item in receipt_data.items:
            html += f"""
        <div class="item-row">
            <span class="item-name">{item['name']}</span>
            <span class="item-qty">{item['quantity']} x</span>
            <span class="item-price">£{item['unit_price']:.2f}</span>
            <span class="item-price">£{item['subtotal']:.2f}</span>
        </div>
"""
        
        html += f"""
    </div>
    
    <div class="divider"></div>
    
    <div class="total">
        TOTAL: £{receipt_data.total:.2f}
    </div>
    
    <div class="payment">
        <div>Payment Method: {receipt_data.payment_method.upper()}</div>
"""
        
        if receipt_data.payment_method.lower() == 'cash':
            if receipt_data.cash_given:
                html += f"        <div>Cash Given: £{receipt_data.cash_given:.2f}</div>\n"
            if receipt_data.change:
                html += f"        <div>Change: £{receipt_data.change:.2f}</div>\n"
        
        html += """
    </div>
    
    <div class="footer">
        <p>Thank you for supporting our charity!</p>
        <p>Your purchase helps make a difference.</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_receipt(self, receipt_data: ReceiptData, format: str = 'html',
                    output_dir: str = 'receipts') -> str:
        """
        Save receipt to file
        
        Args:
            receipt_data: ReceiptData object
            format: 'html' or 'text'
            output_dir: Directory to save receipts
        
        Returns:
            Path to saved receipt file
        """
        # Create output directory if needed
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = receipt_data.timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"receipt_{receipt_data.transaction_id}_{timestamp}.{format}"
        filepath = output_path / filename
        
        # Generate content
        if format == 'html':
            content = self.generate_html_receipt(receipt_data)
        elif format == 'text' or format == 'txt':
            content = self.generate_text_receipt(receipt_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)


if __name__ == '__main__':
    # Test receipt generation
    print("Testing Receipt Generation...")
    
    generator = ReceiptGenerator(
        shop_name="The Good Cause Charity Shop",
        shop_address="42 Market Street, Townville, TC1 2AB",
        shop_phone="01234 567890",
        charity_number="987654"
    )
    
    # Create sample receipt data
    receipt_data = ReceiptData(
        transaction_id=123,
        items=[
            {'name': 'Book - The Great Gatsby', 'quantity': 1, 'unit_price': Decimal('3.50'), 'subtotal': Decimal('3.50')},
            {'name': 'Mug', 'quantity': 2, 'unit_price': Decimal('2.00'), 'subtotal': Decimal('4.00')},
            {'name': 'T-Shirt', 'quantity': 1, 'unit_price': Decimal('8.00'), 'subtotal': Decimal('8.00')},
        ],
        total=Decimal('15.50'),
        payment_method='cash',
        cash_given=Decimal('20.00'),
        change=Decimal('4.50'),
        cashier='Alice'
    )
    
    # Generate text receipt
    print("\n1. Text Receipt:")
    print("-" * 60)
    text_receipt = generator.generate_text_receipt(receipt_data)
    print(text_receipt)
    print("-" * 60)
    
    # Save HTML receipt
    print("\n2. Saving HTML receipt...")
    html_path = generator.save_receipt(receipt_data, format='html')
    print(f"   Saved to: {html_path}")
    
    # Save text receipt
    print("\n3. Saving text receipt...")
    text_path = generator.save_receipt(receipt_data, format='text')
    print(f"   Saved to: {text_path}")
    
    print("\n✓ Receipt generation test completed!")



