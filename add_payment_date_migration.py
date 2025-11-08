"""
Database migration script - Add payment_date field to Invoice model

This migration adds:
- payment_date column to invoices table (nullable DateTime)

Run this script:
    python add_payment_date_migration.py
"""

from app import create_app, db
from app.models import Invoice
from datetime import datetime

def migrate():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("DATABASE MIGRATION: Add payment_date to Invoice")
        print("=" * 60)
        
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('invoices')]
            
            if 'payment_date' in columns:
                print("✅ Column 'payment_date' already exists!")
                return
            
            print("\n📋 Adding 'payment_date' column to invoices table...")
            
            # Add column using raw SQL
            with db.engine.connect() as conn:
                conn.execute(db.text(
                    "ALTER TABLE invoices ADD COLUMN payment_date DATETIME"
                ))
                conn.commit()
            
            print("✅ Column added successfully!")
            
            # Update payment_date for invoices that are already paid
            print("\n📋 Updating payment_date for existing paid invoices...")
            
            paid_invoices = Invoice.query.filter_by(status='paid').all()
            count = 0
            
            for invoice in paid_invoices:
                # Set payment_date to the last payment date, or created_at if no payments
                last_payment = invoice.payments.order_by(Invoice.id.desc()).first()
                if last_payment:
                    invoice.payment_date = last_payment.payment_date
                else:
                    invoice.payment_date = invoice.created_at
                count += 1
            
            db.session.commit()
            print(f"✅ Updated {count} paid invoices with payment_date")
            
            print("\n" + "=" * 60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate()
