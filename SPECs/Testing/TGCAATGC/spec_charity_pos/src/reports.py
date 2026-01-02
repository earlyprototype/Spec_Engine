"""
Charity Shop POS - Reporting and Analytics
Generate sales, inventory, and donation reports
"""

from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from database import Transaction, TransactionItem, Item, Category, Donation, get_session


class ReportGenerator:
    """Generates various reports for the charity shop"""
    
    def __init__(self, session: Session = None):
        """
        Initialize report generator
        
        Args:
            session: SQLAlchemy session (creates new if not provided)
        """
        self.session = session or get_session()
        self._own_session = session is None
    
    def __del__(self):
        """Clean up session if we created it"""
        if self._own_session and self.session:
            self.session.close()
    
    # ===== DAILY SALES REPORTS =====
    
    def generate_daily_sales_report(self, report_date: date = None) -> Dict[str, Any]:
        """
        Generate daily sales summary report
        
        Args:
            report_date: Date to report on (default: today)
        
        Returns:
            Dict with sales summary data
        """
        report_date = report_date or date.today()
        
        # Get transactions for the day
        start_time = datetime.combine(report_date, datetime.min.time())
        end_time = datetime.combine(report_date, datetime.max.time())
        
        transactions = self.session.query(Transaction).filter(
            and_(
                Transaction.timestamp >= start_time,
                Transaction.timestamp <= end_time,
                Transaction.status == 'completed'
            )
        ).all()
        
        # Calculate totals
        total_sales = sum(t.total_amount for t in transactions)
        transaction_count = len(transactions)
        
        # Payment method breakdown
        cash_transactions = [t for t in transactions if t.payment_method == 'cash']
        card_transactions = [t for t in transactions if t.payment_method == 'card']
        
        cash_total = sum(t.total_amount for t in cash_transactions)
        card_total = sum(t.total_amount for t in card_transactions)
        
        # Item count
        total_items_sold = sum(
            sum(ti.quantity for ti in t.transaction_items)
            for t in transactions
        )
        
        return {
            'date': report_date.strftime('%Y-%m-%d'),
            'transaction_count': transaction_count,
            'total_sales': float(total_sales),
            'total_items_sold': total_items_sold,
            'average_transaction': float(total_sales / transaction_count) if transaction_count > 0 else 0,
            'payment_breakdown': {
                'cash': {
                    'count': len(cash_transactions),
                    'total': float(cash_total)
                },
                'card': {
                    'count': len(card_transactions),
                    'total': float(card_total)
                }
            }
        }
    
    def format_daily_sales_report(self, report_date: date = None) -> str:
        """
        Generate formatted daily sales report text
        
        Args:
            report_date: Date to report on (default: today)
        
        Returns:
            Formatted report string
        """
        data = self.generate_daily_sales_report(report_date)
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"DAILY SALES REPORT - {data['date']}")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Total Transactions: {data['transaction_count']}")
        lines.append(f"Total Items Sold:   {data['total_items_sold']}")
        lines.append(f"Total Sales:        £{data['total_sales']:.2f}")
        lines.append(f"Average Transaction: £{data['average_transaction']:.2f}")
        lines.append("")
        lines.append("Payment Method Breakdown:")
        lines.append(f"  Cash:  {data['payment_breakdown']['cash']['count']:3} transactions  £{data['payment_breakdown']['cash']['total']:8.2f}")
        lines.append(f"  Card:  {data['payment_breakdown']['card']['count']:3} transactions  £{data['payment_breakdown']['card']['total']:8.2f}")
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # ===== INVENTORY REPORTS =====
    
    def generate_inventory_report(self) -> Dict[str, Any]:
        """
        Generate inventory summary report
        
        Returns:
            Dict with inventory data
        """
        items = self.session.query(Item).all()
        
        # Calculate totals
        total_items = len(items)
        in_stock_items = sum(1 for item in items if item.stock_quantity > 0)
        out_of_stock_items = sum(1 for item in items if item.stock_quantity == 0)
        
        total_stock_quantity = sum(item.stock_quantity for item in items)
        total_value = sum(item.price * item.stock_quantity for item in items)
        
        # Category breakdown
        category_data = {}
        for item in items:
            if item.category:
                cat_name = item.category.name
                if cat_name not in category_data:
                    category_data[cat_name] = {
                        'item_count': 0,
                        'stock_quantity': 0,
                        'value': 0
                    }
                category_data[cat_name]['item_count'] += 1
                category_data[cat_name]['stock_quantity'] += item.stock_quantity
                category_data[cat_name]['value'] += float(item.price * item.stock_quantity)
        
        return {
            'total_items': total_items,
            'in_stock_items': in_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'total_stock_quantity': total_stock_quantity,
            'total_value': float(total_value),
            'categories': category_data
        }
    
    def format_inventory_report(self) -> str:
        """
        Generate formatted inventory report text
        
        Returns:
            Formatted report string
        """
        data = self.generate_inventory_report()
        
        lines = []
        lines.append("=" * 60)
        lines.append("INVENTORY REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Total Items:       {data['total_items']}")
        lines.append(f"In Stock:          {data['in_stock_items']}")
        lines.append(f"Out of Stock:      {data['out_of_stock_items']}")
        lines.append(f"Total Quantity:    {data['total_stock_quantity']}")
        lines.append(f"Total Value:       £{data['total_value']:.2f}")
        lines.append("")
        lines.append("Category Breakdown:")
        lines.append("-" * 60)
        lines.append(f"{'Category':<20} {'Items':>8} {'Quantity':>10} {'Value':>12}")
        lines.append("-" * 60)
        
        for cat_name, cat_data in sorted(data['categories'].items()):
            lines.append(
                f"{cat_name:<20} {cat_data['item_count']:>8} "
                f"{cat_data['stock_quantity']:>10} £{cat_data['value']:>10.2f}"
            )
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # ===== DONATION REPORTS =====
    
    def generate_donation_report(self, start_date: date = None, end_date: date = None) -> Dict[str, Any]:
        """
        Generate donation tracking report
        
        Args:
            start_date: Start date for report period
            end_date: End date for report period
        
        Returns:
            Dict with donation data
        """
        # Default to last 30 days
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        donations = self.session.query(Donation).filter(
            and_(
                Donation.donation_date >= start_date,
                Donation.donation_date <= end_date
            )
        ).all()
        
        total_donations = len(donations)
        total_value = sum(d.total_value or Decimal('0') for d in donations)
        
        # Count items from donations
        items_from_donations = self.session.query(Item).filter(
            Item.donation_id.isnot(None)
        ).all()
        
        return {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'total_donations': total_donations,
            'total_value': float(total_value),
            'items_from_donations': len(items_from_donations),
            'donations': [
                {
                    'id': d.id,
                    'donor_name': d.donor_name or 'Anonymous',
                    'donation_date': d.donation_date.strftime('%Y-%m-%d'),
                    'total_value': float(d.total_value) if d.total_value else 0,
                    'item_count': len([i for i in items_from_donations if i.donation_id == d.id])
                }
                for d in donations
            ]
        }
    
    def format_donation_report(self, start_date: date = None, end_date: date = None) -> str:
        """
        Generate formatted donation report text
        
        Args:
            start_date: Start date for report period
            end_date: End date for report period
        
        Returns:
            Formatted report string
        """
        data = self.generate_donation_report(start_date, end_date)
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"DONATION REPORT")
        lines.append(f"Period: {data['start_date']} to {data['end_date']}")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Total Donations:        {data['total_donations']}")
        lines.append(f"Total Value:            £{data['total_value']:.2f}")
        lines.append(f"Items from Donations:   {data['items_from_donations']}")
        lines.append("")
        
        if data['donations']:
            lines.append("Recent Donations:")
            lines.append("-" * 60)
            lines.append(f"{'Date':<12} {'Donor':<20} {'Value':>10} {'Items':>8}")
            lines.append("-" * 60)
            
            for don in data['donations'][:20]:  # Show last 20
                lines.append(
                    f"{don['donation_date']:<12} {don['donor_name'][:20]:<20} "
                    f"£{don['total_value']:>8.2f} {don['item_count']:>8}"
                )
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # ===== EXPORT FUNCTIONS =====
    
    def export_report_to_csv(self, report_data: Dict[str, Any], filename: str) -> str:
        """
        Export report data to CSV file
        
        Args:
            report_data: Report data dictionary
            filename: Output filename
        
        Returns:
            Path to saved CSV file
        """
        import csv
        from pathlib import Path
        
        # Create reports directory
        output_dir = Path('reports')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        # Simple CSV export
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if isinstance(report_data, dict) and report_data:
                # Get first level keys
                writer = csv.DictWriter(f, fieldnames=report_data.keys())
                writer.writeheader()
                writer.writerow(report_data)
        
        return str(filepath)


if __name__ == '__main__':
    # Test report generation
    print("Testing Report Generation...")
    
    generator = ReportGenerator()
    
    # Daily sales report
    print("\n1. Daily Sales Report:")
    print(generator.format_daily_sales_report())
    
    # Inventory report
    print("\n2. Inventory Report:")
    print(generator.format_inventory_report())
    
    # Donation report
    print("\n3. Donation Report:")
    print(generator.format_donation_report())
    
    print("\n✓ Report generation test completed!")



