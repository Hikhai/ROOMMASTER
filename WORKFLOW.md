# 🔄 LUỒNG HOẠT ĐỘNG CHI TIẾT - ROOMMASTER

## 📋 MỤC LỤC
1. [Kiến trúc tổng quan](#kiến-trúc-tổng-quan)
2. [Luồng xác thực](#luồng-xác-thực)
3. [Luồng quản lý phòng](#luồng-quản-lý-phòng)
4. [Luồng quản lý khách thuê](#luồng-quản-lý-khách-thuê)
5. [Luồng quản lý hóa đơn](#luồng-quản-lý-hóa-đơn)
6. [Luồng thanh toán](#luồng-thanh-toán)
7. [Luồng báo cáo](#luồng-báo-cáo)
8. [Luồng quản lý dịch vụ](#luồng-quản-lý-dịch-vụ)

---

## 🏗️ KIẾN TRÚC TỔNG QUAN

### Kiến trúc MVC + Service Layer

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                      │
│                     Bootstrap 5 + JavaScript                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Request
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              ROUTES (Controllers)                      │  │
│  │  auth.py | rooms.py | tenants.py | invoices.py       │  │
│  │  reports.py | users.py | services.py | main.py       │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────▼─────────────────────────────┐ │
│  │           SERVICES LAYER (Business Logic)              │ │
│  │  room_service | tenant_service | invoice_service      │ │
│  │  payment_service | report_service                      │ │
│  └──────────────────────────┬─────────────────────────────┘ │
│                             │                                │
│  ┌──────────────────────────▼─────────────────────────────┐ │
│  │              MODELS (Database Layer)                   │ │
│  │  User | Room | Tenant | Invoice | Service | Payment   │ │
│  └──────────────────────────┬─────────────────────────────┘ │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ↓
                    ┌──────────────────┐
                    │  SQLite Database  │
                    │  roommaster.db   │
                    └──────────────────┘
```

### Các Component chính

1. **Routes (Controllers)**: Xử lý HTTP requests, validate input, gọi Services
2. **Services**: Business logic, xử lý nghiệp vụ phức tạp
3. **Models**: ORM mapping với database
4. **Templates**: Jinja2 templates render HTML
5. **Static**: CSS, JavaScript, images

---

## 🔐 LUỒNG XÁC THỰC

### 1. Đăng nhập (Login Flow)

```
User nhập username/password
         ↓
GET /auth/login → Hiển thị form đăng nhập
         ↓
User submit form
         ↓
POST /auth/login
         ↓
Validate form (WTForms)
         ↓
Query User từ database
         ↓
Check password hash (werkzeug.security)
         ↓
    ┌────────────┬────────────┐
    │ Valid      │ Invalid    │
    ↓            ↓            
login_user()   Flash error
    ↓            ↓
Store session  Redirect login
    ↓
Redirect dashboard
```

**Code minh họa:**
```python
# app/routes/auth.py
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Sai tên đăng nhập hoặc mật khẩu', 'danger')
    return render_template('auth/login.html', form=form)
```

### 2. Phân quyền (Authorization Flow)

```
User request protected route
         ↓
@login_required decorator check
         ↓
    ┌────────────┬────────────┐
    │ Logged in  │ Not logged │
    ↓            ↓            
Check role     Redirect login
@admin_required
@manager_required
         ↓
    ┌────────────┬────────────┐
    │ Has role   │ No role    │
    ↓            ↓            
Execute route  Return 403
```

**Code minh họa:**
```python
# app/decorators.py
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

---

## 🏠 LUỒNG QUẢN LÝ PHÒNG

### 1. Xem danh sách phòng

```
GET /rooms/
    ↓
@login_required
    ↓
Query all rooms từ DB
    ↓
Count tenants per room
    ↓
Render rooms/list.html
    ↓
Display: Room Number | Area | Price | Status | Tenants Count
```

### 2. Thêm phòng mới

```
GET /rooms/create → Show form
    ↓
User fills: room_number, area, price, floor, description
    ↓
POST /rooms/create
    ↓
Validate form
    ↓
Check duplicate room_number
    ↓
    ┌────────────┬────────────┐
    │ Unique     │ Duplicate  │
    ↓            ↓            
Create Room    Flash error
    ↓
room_service.create_room()
    ↓
db.session.add(room)
db.session.commit()
    ↓
Flash success
    ↓
Redirect /rooms/
```

**Code minh họa:**
```python
# app/services/room_service.py
def create_room(room_number, area, price, floor=1, description=None):
    # Check duplicate
    existing = Room.query.filter_by(room_number=room_number).first()
    if existing:
        raise ValueError(f"Phòng {room_number} đã tồn tại")
    
    # Create room
    room = Room(
        room_number=room_number,
        area=area,
        price=price,
        floor=floor,
        description=description,
        status='available'
    )
    db.session.add(room)
    db.session.commit()
    return room
```

### 3. Cập nhật trạng thái phòng

```
Tenant check-in/check-out
    ↓
room_service.update_room_status(room_id)
    ↓
Count active tenants in room
    ↓
    ┌────────────┬────────────┐
    │ Has tenant │ No tenant  │
    ↓            ↓            
status='occupied'  status='available'
    ↓
db.session.commit()
```

---

## 👥 LUỒNG QUẢN LÝ KHÁCH THUÊ

### 1. Thêm khách thuê (Check-in)

```
GET /tenants/add
    ↓
Show form with available rooms dropdown
    ↓
User fills: full_name, phone, id_number, room_id, check_in_date, deposit
    ↓
POST /tenants/add
    ↓
Validate form
    ↓
tenant_service.check_in()
    ↓
┌─────────────────────────────────────┐
│ 1. Create Tenant                    │
│ 2. Update Room status='occupied'    │
│ 3. Commit transaction               │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /tenants/
```

**Code minh họa:**
```python
# app/services/tenant_service.py
def check_in(full_name, phone, id_number, room_id, check_in_date, deposit, **kwargs):
    room = Room.query.get_or_404(room_id)
    
    # Create tenant
    tenant = Tenant(
        full_name=full_name,
        phone=phone,
        id_number=id_number,
        room_id=room_id,
        check_in_date=check_in_date,
        deposit=deposit,
        **kwargs
    )
    db.session.add(tenant)
    
    # Update room status
    room.status = 'occupied'
    
    db.session.commit()
    logger.info(f"Tenant {full_name} checked in to Room {room.room_number}")
    return tenant
```

### 2. Checkout khách thuê

```
POST /tenants/<id>/checkout
    ↓
tenant_service.check_out(tenant_id, check_out_date)
    ↓
┌─────────────────────────────────────┐
│ 1. Set tenant.check_out_date        │
│ 2. Check if room has other tenants  │
│ 3. Update room status if empty      │
│ 4. Commit transaction               │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /tenants/
```

---

## 🧾 LUỒNG QUẢN LÝ HÓA ĐƠN

### 1. Tạo hóa đơn đơn lẻ

```
GET /invoices/create
    ↓
Show form: Select room, month, year
    ↓
User selects room and inputs:
- electric_old, electric_new, electric_unit_price
- water_old, water_new, water_unit_price
- other_fees
    ↓
POST /invoices/create
    ↓
invoice_service.create_invoice()
    ↓
┌─────────────────────────────────────┐
│ 1. Check duplicate (room+month+year)│
│ 2. Calculate amounts:               │
│    - electric = (new-old) * price   │
│    - water = (new-old) * price      │
│    - total = room_price + electric  │
│              + water + other_fees   │
│ 3. Create Invoice                   │
│ 4. Set status='unpaid'              │
│ 5. Commit                           │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /invoices/<id>
```

**Code minh họa:**
```python
# app/services/invoice_service.py
def create_invoice(room_id, month, year, **kwargs):
    # Check duplicate
    existing = Invoice.query.filter_by(
        room_id=room_id, month=month, year=year
    ).first()
    if existing:
        raise ValueError(f"Hóa đơn tháng {month}/{year} cho phòng này đã tồn tại")
    
    room = Room.query.get_or_404(room_id)
    tenant = Tenant.query.filter_by(room_id=room_id, check_out_date=None).first()
    
    # Calculate electric
    electric_old = kwargs.get('electric_old', 0)
    electric_new = kwargs.get('electric_new', 0)
    electric_unit_price = kwargs.get('electric_unit_price', 3500)
    electric_amount = (electric_new - electric_old) * electric_unit_price
    
    # Calculate water
    water_old = kwargs.get('water_old', 0)
    water_new = kwargs.get('water_new', 0)
    water_unit_price = kwargs.get('water_unit_price', 20000)
    water_amount = (water_new - water_old) * water_unit_price
    
    # Calculate total
    total_amount = room.price + electric_amount + water_amount + kwargs.get('other_fees', 0)
    
    # Create invoice
    invoice = Invoice(
        room_id=room_id,
        tenant_id=tenant.id if tenant else None,
        month=month,
        year=year,
        room_price=room.price,
        electric_old=electric_old,
        electric_new=electric_new,
        electric_unit_price=electric_unit_price,
        electric_amount=electric_amount,
        water_old=water_old,
        water_new=water_new,
        water_unit_price=water_unit_price,
        water_amount=water_amount,
        other_fees=kwargs.get('other_fees', 0),
        total_amount=total_amount,
        paid_amount=0,
        status='unpaid'
    )
    
    db.session.add(invoice)
    db.session.commit()
    logger.info(f"Invoice created for Room {room.room_number} - {month}/{year}")
    return invoice
```

### 2. Tạo hóa đơn hàng loạt

```
GET /invoices/create_bulk
    ↓
Show form: month, year
    ↓
User submits
    ↓
POST /invoices/create_bulk
    ↓
invoice_service.create_bulk_invoices(month, year)
    ↓
┌─────────────────────────────────────┐
│ 1. Query all occupied rooms         │
│ 2. For each room:                   │
│    - Check if invoice exists        │
│    - If not, create with defaults:  │
│      * Get tenant info              │
│      * Use previous month readings  │
│      * Calculate total              │
│    - Add to batch                   │
│ 3. Bulk commit all invoices         │
└─────────────────────────────────────┘
    ↓
Flash: "Đã tạo X hóa đơn, bỏ qua Y đã tồn tại"
    ↓
Redirect /invoices/
```

**Code minh họa:**
```python
# app/services/invoice_service.py
def create_bulk_invoices(month, year):
    occupied_rooms = Room.query.filter_by(status='occupied').all()
    created = 0
    skipped = 0
    
    for room in occupied_rooms:
        # Check if invoice already exists
        existing = Invoice.query.filter_by(
            room_id=room.id, month=month, year=year
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        tenant = Tenant.query.filter_by(room_id=room.id, check_out_date=None).first()
        
        # Get previous month invoice for readings
        prev_invoice = Invoice.query.filter_by(room_id=room.id).order_by(
            Invoice.year.desc(), Invoice.month.desc()
        ).first()
        
        electric_old = prev_invoice.electric_new if prev_invoice else 0
        water_old = prev_invoice.water_new if prev_invoice else 0
        
        # Create invoice with default values
        invoice = Invoice(
            room_id=room.id,
            tenant_id=tenant.id if tenant else None,
            month=month,
            year=year,
            room_price=room.price,
            electric_old=electric_old,
            electric_new=electric_old,  # Needs manual update
            water_old=water_old,
            water_new=water_old,  # Needs manual update
            total_amount=room.price,
            paid_amount=0,
            status='unpaid'
        )
        db.session.add(invoice)
        created += 1
    
    db.session.commit()
    logger.info(f"Bulk invoices: {created} created, {skipped} skipped")
    return created, skipped
```

---

## 💰 LUỒNG THANH TOÁN

### 1. Ghi nhận thanh toán

```
GET /invoices/<id>/payment
    ↓
Show payment form:
- Current invoice total
- Already paid amount
- Remaining amount
- Input: amount, payment_method, notes
    ↓
POST /invoices/<id>/payment
    ↓
payment_service.record_payment()
    ↓
┌─────────────────────────────────────┐
│ 1. Validate amount > 0              │
│ 2. Create Payment record            │
│ 3. Update invoice.paid_amount       │
│ 4. Update invoice status:           │
│    - paid_amount == total → 'paid'  │
│    - paid_amount > 0 → 'partial'    │
│    - paid_amount == 0 → 'unpaid'    │
│ 5. Set payment_date if fully paid   │
│ 6. Commit transaction               │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /invoices/<id>
```

**Code minh họa:**
```python
# app/services/payment_service.py
def record_payment(invoice_id, amount, payment_method, notes=None, created_by=None):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if amount <= 0:
        raise ValueError("Số tiền thanh toán phải lớn hơn 0")
    
    remaining = invoice.total_amount - invoice.paid_amount
    if amount > remaining:
        raise ValueError(f"Số tiền thanh toán vượt quá số tiền còn lại: {remaining:,.0f}đ")
    
    # Create payment record
    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        payment_method=payment_method,
        notes=notes,
        created_by=created_by or current_user.id
    )
    db.session.add(payment)
    
    # Update invoice
    invoice.paid_amount += amount
    
    # Update status
    if invoice.paid_amount >= invoice.total_amount:
        invoice.status = 'paid'
        invoice.payment_date = datetime.utcnow()
    elif invoice.paid_amount > 0:
        invoice.status = 'partial'
    
    db.session.commit()
    logger.info(f"Payment {amount:,.0f}đ recorded for Invoice {invoice.id}")
    return payment
```

### 2. Xóa thanh toán (Rollback)

```
POST /invoices/payment/<payment_id>/delete
    ↓
payment_service.delete_payment()
    ↓
┌─────────────────────────────────────┐
│ 1. Get payment record               │
│ 2. Subtract amount from invoice     │
│ 3. Recalculate invoice status       │
│ 4. Delete payment                   │
│ 5. Commit                           │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /invoices/<invoice_id>
```

---

## 📊 LUỒNG BÁO CÁO

### 1. Báo cáo doanh thu

```
GET /reports/revenue?month=11&year=2025
    ↓
report_service.get_revenue_report(month, year)
    ↓
┌─────────────────────────────────────┐
│ Query invoices where:               │
│ - month = input_month               │
│ - year = input_year                 │
│                                     │
│ Calculate:                          │
│ - total_invoices = count            │
│ - total_revenue = sum(total_amount) │
│ - paid_revenue = sum(paid_amount)   │
│ - unpaid = total - paid             │
│                                     │
│ Group by room for details           │
└─────────────────────────────────────┘
    ↓
Render reports/revenue.html
    ↓
Display: Chart + Table
```

### 2. Báo cáo tỷ lệ lấp đầy

```
GET /reports/occupancy
    ↓
report_service.get_occupancy_report()
    ↓
┌─────────────────────────────────────┐
│ Count rooms by status:              │
│ - total_rooms                       │
│ - occupied_rooms                    │
│ - available_rooms                   │
│ - maintenance_rooms                 │
│                                     │
│ Calculate:                          │
│ - occupancy_rate = (occupied/total)*100│
│                                     │
│ Get room details with tenant info   │
└─────────────────────────────────────┘
    ↓
Render reports/occupancy.html
    ↓
Display: Stats cards + Room list
```

---

## ⚙️ LUỒNG QUẢN LÝ DỊCH VỤ

### 1. Thêm dịch vụ (Admin only)

```
GET /services/create
    ↓
@admin_required
    ↓
Show form: name, unit, price, description
    ↓
POST /services/create
    ↓
Validate form
    ↓
Check duplicate name
    ↓
┌─────────────────────────────────────┐
│ 1. Create Service                   │
│ 2. Set is_active = True             │
│ 3. Commit                           │
└─────────────────────────────────────┘
    ↓
Flash success
    ↓
Redirect /services/
```

### 2. Toggle trạng thái dịch vụ

```
POST /services/<id>/toggle
    ↓
Get service by id
    ↓
service.is_active = not service.is_active
    ↓
db.session.commit()
    ↓
Flash success
    ↓
Redirect /services/
```

---

## 🎨 LUỒNG GIAO DIỆN (UI)

### Dark Mode Toggle

```
User clicks theme toggle button
    ↓
JavaScript: toggleTheme()
    ↓
Get current theme from localStorage
    ↓
    ┌────────────┬────────────┐
    │ light      │ dark       │
    ↓            ↓            
Set 'dark'     Set 'light'
    ↓            ↓
document.documentElement.setAttribute('data-theme', newTheme)
    ↓
localStorage.setItem('theme', newTheme)
    ↓
Update icon (moon ↔ sun)
    ↓
CSS variables auto-update
```

**Code minh họa:**
```javascript
// app/static/js/main.js
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

// Load theme on page load
document.addEventListener('DOMContentLoaded', loadTheme);
```

---

## 🔄 ERROR HANDLING FLOW

### Xử lý lỗi tập trung

```
Exception occurs in route
    ↓
Flask error handler catches
    ↓
┌────────────────────────────────────┐
│ 404 Not Found                      │
│ → errors.not_found_error()         │
│ → Render errors/404.html           │
├────────────────────────────────────┤
│ 403 Forbidden                      │
│ → errors.forbidden_error()         │
│ → Render errors/403.html           │
├────────────────────────────────────┤
│ 500 Internal Server Error          │
│ → errors.internal_error()          │
│ → Log error                        │
│ → Render errors/500.html           │
└────────────────────────────────────┘
```

**Code minh họa:**
```python
# app/errors.py
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500
```

---

## 📝 LOGGING FLOW

```
Application action occurs
    ↓
logger.info/warning/error()
    ↓
┌────────────────────────────────────┐
│ RotatingFileHandler                │
│ - Max 10MB per file                │
│ - Keep 10 backup files             │
│ - Format: timestamp | level | msg  │
└────────────────────────────────────┘
    ↓
Write to logs/roommaster.log
    ↓
Can be monitored for debugging
```

---

## 🔒 TRANSACTION MANAGEMENT

### Database Transaction Pattern

```python
try:
    # Multiple operations
    db.session.add(obj1)
    db.session.add(obj2)
    db.session.commit()
    
except Exception as e:
    db.session.rollback()
    logger.error(f"Transaction failed: {e}")
    raise
```

### Example: Check-in với transaction

```python
def check_in(tenant_data):
    try:
        # 1. Create tenant
        tenant = Tenant(**tenant_data)
        db.session.add(tenant)
        
        # 2. Update room
        room = Room.query.get(tenant_data['room_id'])
        room.status = 'occupied'
        
        # 3. Commit cả 2 thay đổi
        db.session.commit()
        
        return tenant
        
    except Exception as e:
        # Rollback nếu có lỗi
        db.session.rollback()
        logger.error(f"Check-in failed: {e}")
        raise
```

---

## 🎯 KẾT LUẬN

Hệ thống RoomMaster được xây dựng với:

✅ **Kiến trúc rõ ràng**: MVC + Service Layer  
✅ **Separation of Concerns**: Mỗi layer có trách nhiệm riêng  
✅ **Error Handling**: Xử lý lỗi tập trung  
✅ **Transaction Management**: Đảm bảo tính toàn vẹn dữ liệu  
✅ **Logging**: Ghi nhận hoạt động để debug  
✅ **Authorization**: Phân quyền chặt chẽ  
✅ **UI/UX**: Dark mode, responsive, toast notifications  

Mỗi chức năng đều tuân theo pattern nhất quán, dễ maintain và mở rộng.
