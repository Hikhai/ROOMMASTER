"""
Production Optimization Script
- Add database indexes
- Optimize queries
- Clean up unused data
"""
import sys
from app import create_app, db
from app.models import User, Room, Tenant, Invoice, Payment, Service

def add_indexes():
    """Add indexes to improve query performance"""
    print("📊 Adding database indexes...")
    
    with db.engine.connect() as conn:
        # User indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)'))
            print("✅ User indexes created")
        except Exception as e:
            print(f"⚠️  User indexes: {e}")
        
        # Room indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_rooms_status ON rooms(status)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_rooms_floor ON rooms(floor)'))
            print("✅ Room indexes created")
        except Exception as e:
            print(f"⚠️  Room indexes: {e}")
        
        # Tenant indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_tenants_room_id ON tenants(room_id)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_tenants_check_out_date ON tenants(check_out_date)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_tenants_phone ON tenants(phone)'))
            print("✅ Tenant indexes created")
        except Exception as e:
            print(f"⚠️  Tenant indexes: {e}")
        
        # Invoice indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_invoices_room_id ON invoices(room_id)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_invoices_tenant_id ON invoices(tenant_id)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_invoices_month_year ON invoices(month, year)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date)'))
            print("✅ Invoice indexes created")
        except Exception as e:
            print(f"⚠️  Invoice indexes: {e}")
        
        # Payment indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_payments_invoice_id ON payments(invoice_id)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_payments_payment_date ON payments(payment_date)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_payments_payment_method ON payments(payment_method)'))
            print("✅ Payment indexes created")
        except Exception as e:
            print(f"⚠️  Payment indexes: {e}")
        
        # Service indexes
        try:
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_services_is_active ON services(is_active)'))
            conn.execute(db.text('CREATE INDEX IF NOT EXISTS idx_services_name ON services(name)'))
            print("✅ Service indexes created")
        except Exception as e:
            print(f"⚠️  Service indexes: {e}")
        
        conn.commit()

def optimize_database():
    """Optimize database for production"""
    print("\n🔧 Optimizing database...")
    
    with db.engine.connect() as conn:
        # SQLite specific optimizations
        if 'sqlite' in str(db.engine.url):
            try:
                conn.execute(db.text('PRAGMA journal_mode=WAL'))  # Write-Ahead Logging
                conn.execute(db.text('PRAGMA synchronous=NORMAL'))  # Faster writes
                conn.execute(db.text('PRAGMA cache_size=10000'))  # Increase cache
                conn.execute(db.text('PRAGMA temp_store=MEMORY'))  # Store temp tables in memory
                conn.execute(db.text('VACUUM'))  # Clean up database
                conn.execute(db.text('ANALYZE'))  # Update statistics
                print("✅ SQLite optimizations applied")
            except Exception as e:
                print(f"⚠️  SQLite optimization: {e}")
        
        conn.commit()

def check_statistics():
    """Display database statistics"""
    print("\n📈 Database Statistics:")
    print(f"Users: {User.query.count()}")
    print(f"Rooms: {Room.query.count()}")
    print(f"Tenants: {Tenant.query.count()}")
    print(f"Invoices: {Invoice.query.count()}")
    print(f"Payments: {Payment.query.count()}")
    print(f"Services: {Service.query.count()}")

def main():
    """Main optimization function"""
    print("=" * 60)
    print("🚀 RoomMaster Production Optimization")
    print("=" * 60)
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        try:
            # Add indexes
            add_indexes()
            
            # Optimize database
            optimize_database()
            
            # Show statistics
            check_statistics()
            
            print("\n" + "=" * 60)
            print("✅ Optimization completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error during optimization: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
