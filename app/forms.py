from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, FloatField, IntegerField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, \
    Length, Optional, NumberRange, Regexp
from app.models import User, Room, Tenant


# ==================== Authentication Forms ====================

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')


class RegisterForm(FlaskForm):
    """Registration form - hỗ trợ cả thêm mới và chỉnh sửa"""
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(), 
        Length(min=3, max=80)
    ])
    full_name = StringField('Họ và tên', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Vai trò', choices=[
        ('viewer', 'Viewer - Chỉ xem'),
        ('manager', 'Manager - Quản lý'),
        ('admin', 'Admin - Toàn quyền')
    ], default='manager')
    password = PasswordField('Mật khẩu', validators=[
        Optional(),
        Length(min=6, message='Mật khẩu phải có ít nhất 6 ký tự')
    ])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[
        Optional(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    submit = SubmitField('Lưu')
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        # Bỏ qua nếu username không thay đổi (đang edit)
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Tên đăng nhập đã tồn tại.')
    
    def validate_email(self, email):
        # Bỏ qua nếu email không thay đổi (đang edit)
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email đã được sử dụng.')
    
    def validate_password(self, password):
        # Khi thêm mới: bắt buộc nhập password
        # Khi edit: password có thể để trống (giữ nguyên password cũ)
        if not self.original_username and not password.data:
            raise ValidationError('Mật khẩu không được để trống.')


# ==================== Room Forms ====================

class RoomForm(FlaskForm):
    """Form for creating/editing rooms"""
    room_number = StringField('Số phòng', validators=[
        DataRequired(), 
        Length(max=20)
    ])
    floor = IntegerField('Tầng', validators=[Optional()])
    area = FloatField('Diện tích (m²)', validators=[Optional()])
    price = FloatField('Giá thuê/tháng', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    deposit = FloatField('Tiền cọc', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    status = SelectField('Trạng thái', choices=[
        ('available', 'Còn trống'),
        ('occupied', 'Đã cho thuê'),
        ('maintenance', 'Bảo trì')
    ])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Lưu')
    
    def __init__(self, original_room_number=None, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.original_room_number = original_room_number
    
    def validate_room_number(self, room_number):
        if room_number.data != self.original_room_number:
            room = Room.query.filter_by(room_number=room_number.data).first()
            if room:
                raise ValidationError('Số phòng đã tồn tại.')


# ==================== Tenant Forms ====================

class TenantForm(FlaskForm):
    """Form for creating/editing tenants"""
    room_id = SelectField('Phòng', coerce=int, validators=[DataRequired()])
    full_name = StringField('Họ và tên', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    id_number = StringField('CMND/CCCD', validators=[
        DataRequired(), 
        Length(min=9, max=12, message='CMND/CCCD phải từ 9-12 số'),
        Regexp(r'^\d+$', message='CMND/CCCD chỉ được chứa số')
    ])
    phone = StringField('Số điện thoại', validators=[
        DataRequired(),
        Length(min=10, max=11, message='Số điện thoại phải 10-11 số'),
        Regexp(r'^0\d{9,10}$', message='Số điện thoại không hợp lệ (phải bắt đầu bằng 0)')
    ])
    email = StringField('Email', validators=[Optional(), Email()])
    date_of_birth = StringField('Ngày sinh', validators=[
        Optional(),
        Regexp(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', message='Ngày sinh phải đúng định dạng dd/mm/yyyy')
    ])
    hometown = StringField('Quê quán', validators=[Length(max=200)])
    move_in_date = StringField('Ngày vào ở', validators=[
        DataRequired(),
        Regexp(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', message='Ngày vào ở phải đúng định dạng dd/mm/yyyy')
    ])
    move_out_date = StringField('Ngày chuyển đi', validators=[
        Optional(),
        Regexp(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', message='Ngày chuyển đi phải đúng định dạng dd/mm/yyyy')
    ])
    deposit = DecimalField('Tiền cọc', validators=[Optional(), NumberRange(min=0, message='Tiền cọc không được âm')], places=0, default=0)
    is_main_tenant = BooleanField('Người thuê chính')
    status = SelectField('Trạng thái', choices=[
        ('active', 'Đang ở'),
        ('moved_out', 'Đã chuyển đi')
    ])
    notes = TextAreaField('Ghi chú')
    submit = SubmitField('Lưu')
    
    def __init__(self, original_id_number=None, original_phone=None, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.original_id_number = original_id_number
        self.original_phone = original_phone
    
    def validate_id_number(self, id_number):
        if id_number.data != self.original_id_number:
            tenant = Tenant.query.filter_by(id_number=id_number.data).first()
            if tenant:
                raise ValidationError('Số CMND/CCCD đã tồn tại.')
    
    def validate_phone(self, phone):
        if phone.data != self.original_phone:
            tenant = Tenant.query.filter_by(phone=phone.data).first()
            if tenant:
                raise ValidationError('Số điện thoại đã được sử dụng.')


# ==================== Service Forms ====================

class ServiceForm(FlaskForm):
    """Form for creating/editing services"""
    name = StringField('Tên dịch vụ', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    unit = StringField('Đơn vị', validators=[Length(max=20)])
    price = FloatField('Đơn giá', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    description = TextAreaField('Mô tả')
    is_active = BooleanField('Đang hoạt động')
    submit = SubmitField('Lưu')


# ==================== Invoice Forms ====================

class InvoiceForm(FlaskForm):
    """Form for creating invoices"""
    room_id = SelectField('Phòng', coerce=int, validators=[DataRequired()])
    month = IntegerField('Tháng', validators=[
        DataRequired(),
        NumberRange(min=1, max=12)
    ])
    year = IntegerField('Năm', validators=[DataRequired()])
    room_charge = FloatField('Tiền phòng', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    due_date = DateField('Hạn thanh toán', validators=[Optional()], format='%Y-%m-%d')
    notes = TextAreaField('Ghi chú')
    submit = SubmitField('Tạo hóa đơn')


class InvoiceItemForm(FlaskForm):
    """Form for adding invoice items"""
    service_id = SelectField('Dịch vụ', coerce=int, validators=[DataRequired()])
    old_reading = FloatField('Chỉ số cũ', validators=[Optional()])
    new_reading = FloatField('Chỉ số mới', validators=[Optional()])
    quantity = FloatField('Số lượng', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    unit_price = FloatField('Đơn giá', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    submit = SubmitField('Thêm')


# ==================== Payment Forms ====================

class PaymentForm(FlaskForm):
    """Form for recording payments"""
    amount = FloatField('Số tiền', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    payment_method = SelectField('Phương thức thanh toán', choices=[
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('momo', 'Ví MoMo'),
        ('zalopay', 'ZaloPay'),
        ('other', 'Khác')
    ])
    payment_date = DateField('Ngày thanh toán', validators=[DataRequired()], format='%Y-%m-%d')
    reference_number = StringField('Mã giao dịch', validators=[Length(max=100)])
    notes = TextAreaField('Ghi chú')
    submit = SubmitField('Lưu')
