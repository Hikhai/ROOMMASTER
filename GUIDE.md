# HƯỚNG DẪN SỬ DỤNG ROOMMASTER

## 🚀 KHỞI ĐỘNG ỨNG DỤNG

### Cách 1: Chạy trực tiếp
```bash
python run.py
```

### Cách 2: Dùng Flask CLI
```bash
flask run
```

Truy cập: **http://127.0.0.1:5000**

---

## 🗄️ QUẢN LÝ DATABASE

### Khởi tạo database
```bash
flask init-db
```

### Tạo dữ liệu mẫu
```bash
flask seed-db
```

**Tài khoản admin mặc định:**
- Username: `admin`
- Password: `admin123`

### Test trong Flask Shell
```bash
flask shell
```

**Ví dụ commands:**
```python
# Xem tất cả user
>>> User.query.all()

# Tạo user mới
>>> user = User(username='test', email='test@test.com', full_name='Test User')
>>> user.set_password('123456')
>>> db.session.add(user)
>>> db.session.commit()

# Xem tất cả phòng
>>> Room.query.all()

# Tìm phòng theo số
>>> room = Room.query.filter_by(room_number='P01').first()
>>> print(room.price)

# Tạo phòng mới
>>> room = Room(room_number='P11', price=3000000, floor=3, area=30)
>>> db.session.add(room)
>>> db.session.commit()
```

---

## 📊 CẤU TRÚC DATABASE

### Bảng Users
- Quản lý tài khoản đăng nhập
- Phân quyền: admin, manager, viewer

### Bảng Rooms
- Thông tin phòng trọ
- Trạng thái: available, occupied, maintenance

### Bảng Tenants
- Thông tin khách thuê
- Liên kết với phòng (Foreign Key)

### Bảng Services
- Dịch vụ: điện, nước, internet...
- Đơn giá cho từng dịch vụ

### Bảng Invoices
- Hóa đơn hàng tháng
- Tính toán tự động tổng tiền

### Bảng Invoice_Items
- Chi tiết dịch vụ trong hóa đơn
- Lưu chỉ số điện, nước

### Bảng Payments
- Lịch sử thanh toán
- Hỗ trợ thanh toán từng phần

---

## 🔧 MIGRATION DATABASE

### Khởi tạo migration (lần đầu)
```bash
flask db init
```

### Tạo migration mới khi thay đổi models
```bash
flask db migrate -m "Mô tả thay đổi"
```

### Áp dụng migration
```bash
flask db upgrade
```

### Rollback migration
```bash
flask db downgrade
```

---

## 📝 WORKFLOW SỬ DỤNG

### 1. Thêm phòng mới
Dashboard → Phòng → Thêm phòng mới

### 2. Thêm khách thuê
Dashboard → Khách thuê → Thêm khách thuê
- Chọn phòng trống
- Nhập thông tin CCCD, SĐT
- Phòng tự động chuyển trạng thái "Đã cho thuê"

### 3. Tạo hóa đơn
Dashboard → Hóa đơn → Tạo hóa đơn mới
- Chọn phòng
- Nhập tháng/năm
- Tiền phòng tự động lấy từ Room.price

### 4. Thêm dịch vụ vào hóa đơn
Xem chi tiết hóa đơn → Thêm dịch vụ
- Chọn loại dịch vụ (điện, nước...)
- Nhập chỉ số cũ/mới (hoặc số lượng)
- Hệ thống tự tính thành tiền

### 5. Ghi nhận thanh toán
Xem chi tiết hóa đơn → Thanh toán
- Nhập số tiền
- Chọn phương thức (tiền mặt/chuyển khoản)
- Hóa đơn tự động cập nhật trạng thái

### 6. Xem báo cáo
Dashboard → Báo cáo
- Doanh thu theo tháng
- Tỷ lệ lấp đầy phòng
- Danh sách nợ quá hạn

---

## 🎨 CUSTOM GIAO DIỆN

### CSS
Sửa file: `app/static/css/style.css`

### JavaScript
Sửa file: `app/static/js/main.js`

### Templates
Thư mục: `app/templates/`

---

## 🔐 BẢO MẬT

### Thay đổi SECRET_KEY
File `.env`:
```env
SECRET_KEY=your-random-secret-key-here-min-32-chars
```

**Tạo SECRET_KEY ngẫu nhiên:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Quyền truy cập
- Tất cả trang yêu cầu đăng nhập (@login_required)
- Phân quyền theo User.role

---

## 🐛 TROUBLESHOOTING

### Lỗi: Database is locked
```bash
# Xóa file database và tạo lại
rm roommaster.db
flask init-db
flask seed-db
```

### Lỗi: Import error
```bash
# Kiểm tra virtual environment đã active chưa
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: Template not found
```bash
# Kiểm tra cấu trúc thư mục templates/
tree app/templates
```

---

## 📚 TÀI LIỆU THAM KHẢO

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask-Login: https://flask-login.readthedocs.io/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/

---

## 💡 TIPS

### 1. Backup Database
```bash
# Backup
cp roommaster.db roommaster_backup_$(date +%Y%m%d).db

# Restore
cp roommaster_backup_20240115.db roommaster.db
```

### 2. Export Database to SQL
```bash
sqlite3 roommaster.db .dump > backup.sql
```

### 3. Import từ SQL
```bash
sqlite3 roommaster.db < backup.sql
```

### 4. Xem log errors
```bash
# Windows
$env:FLASK_ENV="development"
flask run

# Linux/Mac
export FLASK_ENV=development
flask run
```

---

## 🎯 NEXT STEPS

1. ✅ Làm quen với giao diện
2. ✅ Thêm 1-2 phòng test
3. ✅ Thêm khách thuê test
4. ✅ Tạo hóa đơn test
5. ✅ Test thanh toán
6. ✅ Xem báo cáo
7. 🚀 Bắt đầu dùng thật!
