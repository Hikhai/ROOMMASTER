"""
Script để tạo dữ liệu mẫu cho RoomMaster
Chạy: python seed_data.py
"""

from app import create_app, db
from app.models import User, Room, Service, Tenant, Invoice
from datetime import date, datetime, timedelta
import random

# Tạo app context
app = create_app()
app.app_context().push()

print('🌱 Đang tạo dữ liệu mẫu...\n')

# Xóa dữ liệu cũ (nếu có)
db.drop_all()
db.create_all()
print('✅ Database đã được tạo mới!')

# 1. Tạo Admin User
print('\n👤 Tạo tài khoản...')
admin = User(
    username='admin',
    email='admin@roommaster.com',
    full_name='Nguyễn Văn Admin',
    role='admin'
)
admin.set_password('admin123')
db.session.add(admin)

# Tạo thêm 1 manager
manager = User(
    username='manager',
    email='manager@roommaster.com',
    full_name='Trần Thị Quản Lý',
    role='manager'
)
manager.set_password('manager123')
db.session.add(manager)

# Tạo viewer
viewer = User(
    username='viewer',
    email='viewer@roommaster.com',
    full_name='Lê Văn Xem',
    role='viewer'
)
viewer.set_password('viewer123')
db.session.add(viewer)

print('   - Admin: admin / admin123 (Toàn quyền)')
print('   - Manager: manager / manager123 (Thêm/Sửa)')
print('   - Viewer: viewer / viewer123 (Chỉ xem)')

# 2. Tạo Services
print('\n🔧 Tạo dịch vụ...')
services = [
    Service(name='Điện', unit='kWh', price=3500, description='Tiền điện sinh hoạt'),
    Service(name='Nước', unit='m³', price=20000, description='Tiền nước sinh hoạt'),
    Service(name='Internet', unit='tháng', price=100000, description='Wifi tốc độ cao'),
    Service(name='Rác', unit='tháng', price=20000, description='Phí vệ sinh môi trường'),
    Service(name='Bảo vệ', unit='tháng', price=50000, description='Phí bảo vệ'),
]

for service in services:
    db.session.add(service)
    print(f'   - {service.name}: {service.price:,.0f} VNĐ/{service.unit}')

db.session.commit()

# 3. Tạo Rooms
print('\n🏠 Tạo phòng trọ...')
rooms_data = [
    # Tầng 1
    ('P101', 1, 25, 2500000, 'occupied'),
    ('P102', 1, 25, 2500000, 'occupied'),
    ('P103', 1, 30, 2800000, 'occupied'),
    ('P104', 1, 25, 2500000, 'available'),
    ('P105', 1, 30, 2800000, 'available'),
    # Tầng 2
    ('P201', 2, 25, 2700000, 'occupied'),
    ('P202', 2, 25, 2700000, 'occupied'),
    ('P203', 2, 30, 3000000, 'available'),
    ('P204', 2, 25, 2700000, 'occupied'),
    ('P205', 2, 30, 3000000, 'available'),
]

rooms = []
for room_number, floor, area, price, status in rooms_data:
    room = Room(
        room_number=room_number,
        floor=floor,
        area=area,
        price=price,
        deposit=price * 2,  # Cọc = 2 tháng tiền phòng
        status=status,
        description=f'Phòng {area}m² tầng {floor}, đầy đủ tiện nghi'
    )
    db.session.add(room)
    rooms.append(room)
    status_text = {'available': '🟢 Trống', 'occupied': '🔴 Đã thuê', 'maintenance': '🟡 Bảo trì'}[status]
    print(f'   - {room.room_number}: {room.price:,.0f} VNĐ/tháng - {area}m² - {status_text}')

db.session.commit()

# 4. Tạo Tenants
print('\n👥 Tạo khách thuê...')
tenants_data = [
    ('Nguyễn Văn An', '001234567890', '0901234567', 'nguyenvanan@email.com', date(1990, 5, 15), 'Hà Nội', 'P101'),
    ('Trần Thị Bình', '001234567891', '0901234568', 'tranthibinh@email.com', date(1992, 8, 20), 'Hải Phòng', 'P102'),
    ('Lê Văn Cường', '001234567892', '0901234569', 'levancuong@email.com', date(1988, 3, 10), 'Đà Nẵng', 'P103'),
    ('Phạm Thị Dung', '001234567893', '0901234570', 'phamthidung@email.com', date(1995, 12, 25), 'TP.HCM', 'P201'),
    ('Hoàng Văn Em', '001234567894', '0901234571', 'hoangvanem@email.com', date(1991, 7, 8), 'Cần Thơ', 'P202'),
    ('Vũ Thị Phượng', '001234567895', '0901234572', 'vuthiphuong@email.com', date(1993, 4, 18), 'Nghệ An', 'P204'),
]

tenants = []
for full_name, id_number, phone, email, dob, hometown, room_number in tenants_data:
    room = Room.query.filter_by(room_number=room_number).first()
    if room:
        move_in = date.today() - timedelta(days=random.randint(30, 180))
        tenant = Tenant(
            full_name=full_name,
            id_number=id_number,
            phone=phone,
            email=email,
            date_of_birth=dob,
            hometown=hometown,
            room_id=room.id,
            move_in_date=move_in,
            deposit=room.deposit,
            is_main_tenant=True,
            status='active',
            notes=f'Khách thuê từ {move_in.strftime("%d/%m/%Y")}'
        )
        db.session.add(tenant)
        tenants.append(tenant)
        print(f'   - {full_name} - {room_number} - SĐT: {phone}')

db.session.commit()
print('\n📊 Thống kê:')
print(f'   - Số user: {User.query.count()} (admin, manager, viewer)')
print(f'   - Số dịch vụ: {Service.query.count()}')
print(f'   - Số phòng: {Room.query.count()}')
print(f'     + Trống: {Room.query.filter_by(status="available").count()}')
print(f'     + Đã thuê: {Room.query.filter_by(status="occupied").count()}')
print(f'   - Số khách thuê: {Tenant.query.count()}')
print(f'   - Số hóa đơn: {Invoice.query.count()}')
print('='*70)
print('\n📊 Thống kê:')
print(f'   - Số user: {User.query.count()}')
print(f'   - Số dịch vụ: {Service.query.count()}')
print(f'   - Số phòng: {Room.query.count()}')
print(f'     + Trống: {Room.query.filter_by(status="available").count()}')
print(f'     + Đã thuê: {Room.query.filter_by(status="occupied").count()}')
print(f'     + Bảo trì: {Room.query.filter_by(status="maintenance").count()}')
print(f'   - Số khách thuê: {Tenant.query.count()}')
print(f'   - Số hóa đơn: {Invoice.query.count()}')
print(f'     + Đã thanh toán: {Invoice.query.filter_by(status="paid").count()}')
print(f'     + Chưa thanh toán: {Invoice.query.filter_by(status="unpaid").count()}')
print(f'     + Thanh toán 1 phần: {Invoice.query.filter_by(status="partial").count()}')

print('\n🚀 Bắt đầu sử dụng:')
print('   1. Chạy: python run.py')
print('   2. Truy cập: http://127.0.0.1:5000')
print('   3. Đăng nhập với một trong các tài khoản:')
print('      - admin / admin123 (Toàn quyền)')
print('\n💡 Dữ liệu cơ bản đã tạo:')
print('   - 3 tài khoản với 3 role khác nhau')
print('   - 5 dịch vụ (Điện, Nước, Internet, Rác, Bảo vệ)')
print('   - 10 phòng trọ (6 phòng đã thuê, 4 phòng trống)')
print('   - 6 khách thuê đang ở')
print('\n📝 Bạn có thể test các chức năng:')
print('   - Tạo hóa đơn đơn lẻ cho phòng đã có khách')
print('   - Tạo hóa đơn hàng loạt (sẽ tạo cho 6 phòng)')
print('   - Test unique constraint (tạo trùng hóa đơn)')
print('   - Test phân quyền với các role khác nhau')
print('\n')
print('   - Test phân quyền với các role khác nhau')
print('\n')
print('\n📊 Thống kê:')
print(f'   - Số user: {User.query.count()} (admin, manager, viewer)')
print(f'   - Số dịch vụ: {Service.query.count()}')
print(f'   - Số phòng: {Room.query.count()} (tất cả đang trống)')
print(f'   - Số khách thuê: {Tenant.query.count()}')
print(f'   - Số hóa đơn: {Invoice.query.count()}')