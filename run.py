import os
from app import create_app, db
from app.models import User, Room, Tenant, Service, Invoice, Payment

# Tạo Flask app
app = create_app()


# Flask shell context - Tự động import khi dùng `flask shell`
@app.shell_context_processor
def make_shell_context():
    """
    Khi chạy 'flask shell', tự động import sẵn các model
    Giúp test nhanh trong terminal
    """
    return {
        'db': db,
        'User': User,
        'Room': Room,
        'Tenant': Tenant,
        'Service': Service,
        'Invoice': Invoice,
        'Payment': Payment
    }


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('✅ Database initialized!')


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from werkzeug.security import generate_password_hash
    from datetime import date
    
    print('🌱 Seeding database...')
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@roommaster.com',
        full_name='Administrator'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create sample services
    services = [
        Service(name='Điện', unit='kWh', price=3500, description='Tiền điện'),
        Service(name='Nước', unit='m³', price=20000, description='Tiền nước'),
        Service(name='Internet', unit='tháng', price=100000, description='Wifi'),
        Service(name='Rác', unit='tháng', price=20000, description='Phí vệ sinh'),
    ]
    for service in services:
        db.session.add(service)
    
    # Create sample rooms
    for i in range(1, 11):
        room = Room(
            room_number=f'P{i:02d}',
            floor=(i-1)//5 + 1,
            area=25.0,
            price=2500000,
            deposit=5000000,
            status='available' if i > 3 else 'occupied',
            description=f'Phòng {i:02d} - Tầng {(i-1)//5 + 1}'
        )
        db.session.add(room)
    
    db.session.commit()
    print('✅ Sample data added!')
    print('👤 Admin account: admin / admin123')


# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True)
