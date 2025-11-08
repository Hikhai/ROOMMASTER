# 🏢 RoomMaster - Hệ thống quản lý phòng trọ chuyên nghiệp

Ứng dụng web quản lý phòng trọ được xây dựng bằng Flask framework, áp dụng kiến trúc MVC với Service Layer pattern để dễ bảo trì và mở rộng.

## ✨ Tính năng nổi bật

### 🔐 Quản lý người dùng & Phân quyền
- **3 cấp độ quyền**: Admin, Manager, Viewer
- Đăng nhập/đăng xuất an toàn với Flask-Login
- Giao diện tự động ẩn/hiện theo quyền
- Session management

### 🏠 Quản lý phòng trọ
- CRUD phòng trọ (thêm, sửa, xóa, xem)
- Theo dõi trạng thái: Trống, Đã thuê, Bảo trì
- Thông tin chi tiết: Diện tích, giá, tầng
- Lịch sử hóa đơn theo phòng

### 👥 Quản lý khách thuê
- Thông tin đầy đủ: CCCD, SĐT, Email, Quê quán
- Theo dõi ngày vào/ra
- Quản lý tiền cọc
- Lịch sử hóa đơn của khách

### 🧾 Quản lý hóa đơn
- **Tạo hóa đơn hàng loạt** cho nhiều phòng cùng lúc
- **Unique constraint**: Mỗi phòng - mỗi tháng - chỉ một hóa đơn
- Tính toán tự động: Tiền phòng + dịch vụ
- Tính năng đọc số: Điện, nước tự động tính
- Trạng thái: Chưa thanh toán, Đã thanh toán, Thanh toán 1 phần

### 💰 Quản lý thanh toán
- **Thanh toán từng phần** được hỗ trợ
- Nhiều phương thức: Tiền mặt, chuyển khoản, ví điện tử
- Lịch sử thanh toán chi tiết
- Tự động cập nhật trạng thái hóa đơn

### 📊 Báo cáo & Thống kê
- **Báo cáo doanh thu**: Theo tháng/năm
- **Báo cáo tỷ lệ lấp đầy**: Phòng trống/đã thuê
- **Báo cáo quá hạn**: Hóa đơn chưa thanh toán
- **Báo cáo khách thuê**: Thống kê khách thuê
- Dashboard tổng quan

### 🎨 Giao diện người dùng
- Responsive design với Bootstrap 5
- **Navbar active tự động** theo trang hiện tại
- **Clickable rows** - Click vào hàng để xem chi tiết
- Toast notifications đẹp mắt
- Loading states & transitions mượt mà

## 🏗️ Kiến trúc dự án (Đã tái cấu trúc)

```
RoomMaster/
├── app/
│   ├── __init__.py              # App factory với error handlers
│   ├── models.py                # Database models (ORM)
│   ├── forms.py                 # WTForms validation
│   ├── errors.py                # ⭐ Error handlers tập trung
│   ├── decorators.py            # Custom decorators
│   │
│   ├── routes/                  # 🎯 Blueprints (Controllers)
│   │   ├── auth.py              # Authentication
│   │   ├── main.py              # Dashboard
│   │   ├── rooms.py             # Quản lý phòng
│   │   ├── tenants.py           # Quản lý khách thuê
│   │   ├── invoices.py          # Quản lý hóa đơn
│   │   ├── reports.py           # Báo cáo thống kê
│   │   └── users.py             # Quản lý nhân viên
│   │
│   ├── services/                # ⭐ Business Logic Layer
│   │   ├── __init__.py
│   │   ├── room_service.py      # Logic nghiệp vụ phòng
│   │   ├── tenant_service.py    # Logic nghiệp vụ khách thuê
│   │   ├── invoice_service.py   # Logic nghiệp vụ hóa đơn
│   │   ├── payment_service.py   # Logic nghiệp vụ thanh toán
│   │   └── report_service.py    # Logic báo cáo
│   │
│   ├── utils/                   # ⭐ Utilities & Helpers
│   │   ├── __init__.py
│   │   ├── helpers.py           # Helper functions
│   │   └── logger.py            # Logging configuration
│   │
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── _macros.html         # Template macros
│   │   ├── auth/
│   │   ├── rooms/
│   │   ├── tenants/
│   │   ├── invoices/
│   │   ├── reports/
│   │   ├── users/
│   │   └── errors/              # ⭐ Error pages (404, 500, 403)
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Custom styles
│       └── js/
│           └── main.js          # Client-side logic
│
├── instance/                    # Instance-specific files
│   └── roommaster.db           # SQLite database
│
├── logs/                        # ⭐ Application logs
│   └── roommaster.log
│
├── migrations/                  # Database migrations
│
├── config.py                   # Configuration classes
├── .env.example                # ⭐ Environment variables template
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── seed_data.py               # Sample data generator
└── README.md                  # This file
```

## 🎯 Design Patterns & Best Practices

### 1. **Service Layer Pattern**
Tách biệt business logic khỏi routes:
```python
# Routes (thin controllers)
@bp.route('/rooms')
def list_rooms():
    rooms = RoomService.get_all_rooms(page=1)
    return render_template('rooms/list.html', rooms=rooms)

# Services (business logic)
class RoomService:
    @staticmethod
    def get_all_rooms(page, per_page=10, search=None):
        query = Room.query
        if search:
            query = query.filter(Room.room_number.ilike(f'%{search}%'))
        return query.paginate(page=page, per_page=per_page)
```

### 2. **Factory Pattern**
App factory cho flexibility và testing:
```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Initialize extensions, blueprints, error handlers...
    return app
```

### 3. **Blueprint Pattern**
Tổ chức routes modular:
```python
bp = Blueprint('rooms', __name__, url_prefix='/rooms')
app.register_blueprint(bp)
```

### 4. **Error Handling**
Centralized error handlers:
```python
@app.errorhandler(404)
def not_found(error):
    logger.info(f'Not Found: {request.url}')
    return render_template('errors/404.html'), 404
```

### 5. **Logging**
Structured logging với rotation:
```python
# Tự động log vào file với rotation (10MB, 10 backups)
app.logger.info('User logged in')
app.logger.error('Database error', exc_info=True)
```

## 📦 Cài đặt chi tiết

### Yêu cầu hệ thống
- Python 3.8+
- pip
- virtualenv (khuyến nghị)

### Bước 1: Clone & Setup
```bash
# Clone repository
git clone <repository-url>
cd RoomMaster

# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình môi trường
```bash
# Copy file .env.example thành .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Chỉnh sửa .env và cập nhật các giá trị:
# - SECRET_KEY (BẮT BUỘC thay đổi trong production!)
# - DATABASE_URL (nếu dùng PostgreSQL/MySQL)
# - Các cấu hình khác...
```

### Bước 4: Khởi tạo database
```bash
# Tạo database
python run.py
# hoặc
flask db upgrade
```

### Bước 5: Tạo dữ liệu mẫu (tùy chọn)
```bash
python seed_data.py
```

Dữ liệu mẫu bao gồm:
- **3 users**: admin (admin/admin123), manager (manager/123456), viewer (viewer/123456)
- **5 services**: Điện, nước, internet, rác, wifi
- **10 rooms**: P01-P10 (6 phòng đã thuê, 4 phòng trống)
- **6 tenants**: Khách thuê mẫu

## 🚀 Chạy ứng dụng

### Development Mode
```bash
python run.py
```

Truy cập: http://127.0.0.1:5000

### Production Mode (với Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

### Tài khoản mặc định
| Username | Password | Role | Quyền |
|----------|----------|------|-------|
| admin | admin123 | Admin | Toàn quyền |
| manager | 123456 | Manager | Quản lý (không xóa) |
| viewer | 123456 | Viewer | Chỉ xem |

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database ORM**: SQLAlchemy 3.1.1
- **Migration**: Flask-Migrate
- **Authentication**: Flask-Login
- **Forms**: WTForms với Flask-WTF
- **Database**: SQLite (dev) / PostgreSQL (production)

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.11.0
- **Template Engine**: Jinja2
- **JavaScript**: Vanilla JS với modern ES6+
- **Date Picker**: Flatpickr

### Development Tools
- **Environment**: python-dotenv
- **Password Hashing**: Werkzeug Security
- **Logging**: Python logging với RotatingFileHandler

## 📋 Database Schema

### User (Người dùng)
```python
- id (PK)
- username (unique)
- email (unique)
- password_hash
- full_name
- role (admin/manager/viewer)
- created_at
```

### Room (Phòng)
```python
- id (PK)
- room_number (unique)
- floor
- area
- price
- deposit
- status (available/occupied/maintenance)
- description
```

### Tenant (Khách thuê)
```python
- id (PK)
- room_id (FK)
- full_name
- id_number (unique)
- phone (unique)
- email
- date_of_birth
- hometown
- move_in_date
- move_out_date
- deposit
- is_main_tenant
- status (active/moved_out)
```

### Invoice (Hóa đơn)
```python
- id (PK)
- room_id (FK)
- month, year (unique với room_id)
- room_charge
- total_amount
- due_date
- status (paid/unpaid/partial)
- notes
- created_at
```

### Payment (Thanh toán)
```python
- id (PK)
- invoice_id (FK)
- amount
- payment_method
- payment_date
- reference_number
- notes
```

## 🎯 API Endpoints (Routes)

### Authentication
- `GET /auth/login` - Trang đăng nhập
- `POST /auth/login` - Xử lý đăng nhập
- `GET /auth/logout` - Đăng xuất
- `GET /auth/register` - Trang đăng ký (Admin only)
- `POST /auth/register` - Xử lý đăng ký

### Dashboard
- `GET /` - Dashboard chính

### Rooms
- `GET /rooms` - Danh sách phòng
- `GET /rooms/add` - Form thêm phòng
- `POST /rooms/add` - Xử lý thêm phòng
- `GET /rooms/<id>` - Chi tiết phòng
- `GET /rooms/<id>/edit` - Form sửa phòng
- `POST /rooms/<id>/edit` - Xử lý sửa phòng
- `POST /rooms/<id>/delete` - Xóa phòng

### Tenants
- `GET /tenants` - Danh sách khách thuê
- `GET /tenants/add` - Form thêm khách
- `POST /tenants/add` - Xử lý thêm khách
- `GET /tenants/<id>` - Chi tiết khách
- `GET /tenants/<id>/edit` - Form sửa khách
- `POST /tenants/<id>/edit` - Xử lý sửa khách
- `POST /tenants/<id>/checkout` - Trả phòng
- `POST /tenants/<id>/delete` - Xóa khách

### Invoices
- `GET /invoices` - Danh sách hóa đơn
- `GET /invoices/create` - Form tạo hóa đơn
- `POST /invoices/create` - Xử lý tạo hóa đơn
- `GET /invoices/create-bulk` - Form tạo hàng loạt
- `POST /invoices/create-bulk` - Xử lý tạo hàng loạt
- `GET /invoices/<id>` - Chi tiết hóa đơn
- `GET /invoices/<id>/edit` - Form sửa hóa đơn
- `POST /invoices/<id>/edit` - Xử lý sửa hóa đơn
- `GET /invoices/<id>/payment` - Form thanh toán
- `POST /invoices/<id>/payment` - Xử lý thanh toán
- `POST /invoices/<id>/delete` - Xóa hóa đơn

### Reports
- `GET /reports` - Trang báo cáo chính
- `GET /reports/revenue` - Báo cáo doanh thu
- `GET /reports/occupancy` - Báo cáo lấp đầy
- `GET /reports/overdue` - Báo cáo quá hạn
- `GET /reports/tenants` - Báo cáo khách thuê

### Users (Admin only)
- `GET /users` - Danh sách nhân viên
- `GET /users/add` - Form thêm nhân viên
- `POST /users/add` - Xử lý thêm nhân viên
- `GET /users/<id>/edit` - Form sửa nhân viên
- `POST /users/<id>/edit` - Xử lý sửa nhân viên
- `POST /users/<id>/delete` - Xóa nhân viên

## 📝 Logging

### Log Levels
- **DEBUG**: Chi tiết development
- **INFO**: Thông tin tổng quát (startup, user actions)
- **WARNING**: Cảnh báo (bad requests, validation errors)
- **ERROR**: Lỗi xử lý (exceptions, database errors)

### Log Location
- **Development**: Console output
- **Production**: `logs/roommaster.log` (với rotation)

### Log Format
```
[2025-11-06 10:30:15] INFO in routes: User admin logged in
[2025-11-06 10:31:22] ERROR in invoices: Database error when creating invoice
```

## 🔒 Security Features

### Implemented
- ✅ Password hashing với Werkzeug
- ✅ CSRF Protection với Flask-WTF
- ✅ Session management với Flask-Login
- ✅ Role-based access control
- ✅ SQL Injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (Jinja2 auto-escaping)

### Recommended for Production
- [ ] HTTPS/SSL certificates
- [ ] Rate limiting
- [ ] Security headers
- [ ] Environment-based secrets
- [ ] Database backups
- [ ] Input sanitization
- [ ] File upload restrictions

## 🧪 Testing (Future Enhancement)

```bash
# Unit tests
pytest tests/unit

# Integration tests  
pytest tests/integration

# Coverage report
pytest --cov=app tests/
```

## 📈 Performance Optimization

### Database
- Indexed columns: username, email, room_number, id_number, phone
- Unique constraints for data integrity
- Lazy loading relationships
- Query optimization với select_related

### Frontend
- Minified CSS/JS (production)
- Image optimization
- Browser caching
- CDN cho Bootstrap, Icons

## 🚢 Deployment

### With Gunicorn (Linux/Mac)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

### With Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

### Environment Variables for Production
```bash
FLASK_ENV=production
SECRET_KEY=<your-random-secret-key>
DATABASE_URL=postgresql://user:pass@localhost/roommaster
```

## 🤝 Contributing

### Quy trình đóng góp
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

### Code Style
- PEP 8 for Python
- ESLint for JavaScript
- Prettier for formatting

## 📄 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết

## 👨‍💻 Authors

**RoomMaster Development Team**
- Email: khaihh.goog@gmail.com
- Website: https://kykhai.pythonanywhere.com/

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Flask-Login](https://flask-login.readthedocs.io/) - User session management
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library

## 📞 Support

Có vấn đề? Mở issue tại [GitHub Issues](https://github.com/hikhai/roommaster/issues)

---

⭐ Star repository này nếu hữu ích!
