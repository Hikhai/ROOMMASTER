from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


# ============================================
# USER LOADER - Flask-Login yêu cầu
# ============================================
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login dùng hàm này để load user từ session
    Được gọi mỗi khi user truy cập trang (nếu đã đăng nhập)
    """
    return User.query.get(int(user_id))


# ============================================
# MODEL 1: USER (Người dùng hệ thống)
# ============================================
class User(UserMixin, db.Model):
    """
    Model User - Quản lý tài khoản đăng nhập
    UserMixin: Cung cấp các method cần thiết cho Flask-Login
    """
    __tablename__ = 'users'
    
    # Các cột (columns)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False, default='User')
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='manager')  # admin, manager, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    invoices = db.relationship('Invoice', backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        """
        Mã hóa mật khẩu trước khi lưu vào DB
        Không bao giờ lưu mật khẩu dạng plain text!
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Kiểm tra mật khẩu khi đăng nhập
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """Hiển thị khi print(user)"""
        return f'<User {self.username}>'


# ============================================
# MODEL 2: ROOM (Phòng trọ)
# ============================================
class Room(db.Model):
    """Model Room - Quản lý thông tin phòng trọ"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    floor = db.Column(db.Integer, default=1)
    area = db.Column(db.Float, default=0)  # Diện tích (m²)
    price = db.Column(db.Float, nullable=False)  # Giá phòng/tháng
    deposit = db.Column(db.Float, default=0)  # Tiền cọc
    status = db.Column(db.String(20), default='available')  # available, occupied, maintenance
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (Quan hệ với bảng khác)
    # backref: Tạo thuộc tính ngược lại (tenant.room)
    # lazy: Cách load dữ liệu (dynamic = query object)
    # cascade: Khi xóa Room → Xóa cả Tenant, Invoice liên quan
    tenants = db.relationship('Tenant', backref='room', lazy='dynamic', cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='room', lazy='dynamic')
    
    def __repr__(self):
        return f'<Room {self.room_number}>'
    
    @property
    def current_tenant(self):
        """
        Lấy khách thuê hiện tại của phòng
        @property: Dùng như thuộc tính (room.current_tenant)
        """
        return self.tenants.filter_by(status='active').first()


# ============================================
# MODEL 3: TENANT (Khách thuê)
# ============================================
class Tenant(db.Model):
    """Model Tenant - Quản lý thông tin khách thuê"""
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(20), unique=True, nullable=False, index=True)  # CMND/CCCD
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date)
    hometown = db.Column(db.String(200))  # Quê quán
    
    # Foreign Key - Liên kết với bảng rooms
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    
    move_in_date = db.Column(db.Date, nullable=False)
    move_out_date = db.Column(db.Date)
    deposit = db.Column(db.Float, default=0)  # Tiền đặt cọc
    is_main_tenant = db.Column(db.Boolean, default=True)  # Người thuê chính
    status = db.Column(db.String(20), default='active')  # active, moved_out
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tenant {self.full_name}>'


# ============================================
# MODEL 4: SERVICE (Dịch vụ)
# ============================================
class Service(db.Model):
    """Model Service - Quản lý các dịch vụ (điện, nước, internet...) - Chỉ lưu đơn giá tham khảo"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20))  # Đơn vị: kWh, m³, tháng...
    price = db.Column(db.Float, nullable=False)  # Đơn giá
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.name}>'


# ============================================
# MODEL 5: INVOICE (Hóa đơn)
# ============================================
class Invoice(db.Model):
    """Model Invoice - Quản lý hóa đơn hàng tháng (Cấu trúc đơn giản với trường trực tiếp)"""
    __tablename__ = 'invoices'
    
    # ✅ UNIQUE CONSTRAINT: MỖI PHÒNG - MỖI THÁNG - CHỈ MỘT HÓA ĐƠN
    __table_args__ = (
        db.UniqueConstraint('room_id', 'month', 'year', name='uq_room_month_year'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Thời gian
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)   # 2024, 2025...
    
    # Tiền phòng
    room_price = db.Column(db.Float, default=0)  # Giá phòng trong tháng
    
    # Chỉ số điện
    electric_old = db.Column(db.Float, default=0)  # Số điện cũ
    electric_new = db.Column(db.Float, default=0)  # Số điện mới
    electric_unit_price = db.Column(db.Float, default=3500)  # Đơn giá điện (VNĐ/kWh)
    
    # Chỉ số nước
    water_old = db.Column(db.Float, default=0)  # Số nước cũ
    water_new = db.Column(db.Float, default=0)  # Số nước mới
    water_unit_price = db.Column(db.Float, default=20000)  # Đơn giá nước (VNĐ/m³)
    
    # Các khoản phí khác
    other_fees = db.Column(db.Float, default=0)  # Rác, internet, xe...
    
    # Tổng tiền (tự động tính)
    total_amount = db.Column(db.Float, default=0)
    
    # Trạng thái
    status = db.Column(db.String(20), default='unpaid')  # unpaid, partial, paid
    
    # Ngày tháng
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)  # Hạn thanh toán
    payment_date = db.Column(db.DateTime)  # Ngày thanh toán đủ (khi status = 'paid')
    
    notes = db.Column(db.Text)  # Ghi chú
    
    # Relationships
    payments = db.relationship('Payment', backref='invoice', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Invoice P{self.room.room_number if self.room else "?"} {self.month}/{self.year}>'
    
    def calculate_total(self):
        """
        Tính tổng tiền hóa đơn
        Công thức: Tiền phòng + Tiền điện + Tiền nước + Phí khác
        
        Returns:
            float: Tổng tiền hóa đơn
        """
        # Tính tiền điện = (Số mới - Số cũ) × Đơn giá
        electric_usage = max(0, self.electric_new - self.electric_old)
        electric_cost = electric_usage * self.electric_unit_price
        
        # Tính tiền nước = (Số mới - Số cũ) × Đơn giá
        water_usage = max(0, self.water_new - self.water_old)
        water_cost = water_usage * self.water_unit_price
        
        # Tổng = Phòng + Điện + Nước + Khác
        self.total_amount = self.room_price + electric_cost + water_cost + self.other_fees
        
        return self.total_amount
    
    @property
    def electric_cost(self):
        """Tiền điện (VNĐ)"""
        usage = max(0, self.electric_new - self.electric_old)
        return usage * self.electric_unit_price
    
    @property
    def water_cost(self):
        """Tiền nước (VNĐ)"""
        usage = max(0, self.water_new - self.water_old)
        return usage * self.water_unit_price
    
    @property
    def paid_amount(self):
        """Tổng số tiền đã thanh toán (VNĐ)"""
        return sum(p.amount for p in self.payments)
    
    @property
    def remaining_amount(self):
        """Số tiền còn nợ (VNĐ)"""
        return max(0, self.total_amount - self.paid_amount)
    
    @property
    def overpaid_amount(self):
        """Số tiền thanh toán thừa (VNĐ)"""
        return max(0, self.paid_amount - self.total_amount)
    
    def update_status(self):
        """
        Cập nhật trạng thái hóa đơn dựa trên số tiền đã thanh toán
        Tự động set payment_date khi thanh toán đủ
        
        Xử lý 3 trường hợp:
        - paid == 0: unpaid
        - 0 < paid < total: partial
        - paid >= total: paid (kể cả thanh toán thừa)
        """
        paid = self.paid_amount
        
        if paid == 0:
            self.status = 'unpaid'
            self.payment_date = None
        elif paid >= self.total_amount:
            self.status = 'paid'
            # Chỉ set payment_date lần đầu tiên khi chuyển sang paid
            if self.payment_date is None:
                self.payment_date = datetime.utcnow()
        else:
            self.status = 'partial'
            self.payment_date = None
    
    @property
    def days_overdue(self):
        """
        Tính số ngày quá hạn
        
        Returns:
            int: Số ngày quá hạn (0 nếu chưa quá hạn hoặc đã thanh toán đủ)
        """
        # Nếu đã thanh toán đủ, không tính quá hạn
        if self.status == 'paid':
            return 0
        
        # Nếu không có due_date, không tính quá hạn
        if not self.due_date:
            return 0
        
        # Tính số ngày từ due_date đến hiện tại
        now = datetime.utcnow()
        if now > self.due_date:
            delta = now - self.due_date
            return delta.days
        
        return 0
    
    @property
    def is_overdue(self):
        """
        Kiểm tra hóa đơn có quá hạn không
        
        Returns:
            bool: True nếu quá hạn và chưa thanh toán đủ
        """
        return self.days_overdue > 0
    
    @property
    def overdue_level(self):
        """
        Phân loại mức độ nợ quá hạn
        
        Returns:
            str: 'ok' (không nợ), 'warning' (1-5 ngày), 'danger' (5-10 ngày), 'critical' (>10 ngày)
        """
        days = self.days_overdue
        
        if days == 0:
            return 'ok'
        elif days <= 5:
            return 'warning'
        elif days <= 10:
            return 'danger'
        else:
            return 'critical'
    
    @property
    def overdue_badge(self):
        """
        Lấy badge HTML cho trạng thái quá hạn
        
        Returns:
            str: HTML badge string
        """
        days = self.days_overdue
        
        if days == 0:
            return ''
        elif days <= 5:
            return f'<span class="badge bg-warning">Quá hạn {days} ngày</span>'
        elif days <= 10:
            return f'<span class="badge bg-danger">Nợ {days} ngày</span>'
        else:
            return f'<span class="badge bg-dark">Nợ xấu {days} ngày</span>'


# ============================================
# MODEL 6: PAYMENT (Thanh toán)
# ============================================
class Payment(db.Model):
    """Model Payment - Quản lý các lần thanh toán"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)  # Số tiền thanh toán
    payment_method = db.Column(db.String(20), default='cash')  # cash, bank_transfer
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)  # Ghi chú
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.amount}đ>'
