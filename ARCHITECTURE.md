# 🏗️ RoomMaster - Kiến trúc hệ thống

Tài liệu này mô tả kiến trúc và design patterns được sử dụng trong RoomMaster.

## 📐 Tổng quan kiến trúc

RoomMaster được xây dựng theo **Layered Architecture** với các layer sau:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│    (Templates + Static Files)           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Controller Layer                │
│         (Routes/Blueprints)             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Service Layer                   │
│       (Business Logic)                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Data Access Layer               │
│     (Models + SQLAlchemy ORM)           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Database                      │
│          (SQLite/PostgreSQL)            │
└─────────────────────────────────────────┘
```

## 🎯 Design Patterns

### 1. Factory Pattern (App Factory)

**File**: `app/__init__.py`

**Mục đích**: Tạo Flask app instance với cấu hình linh hoạt

**Lợi ích**:
- Dễ testing với nhiều config khác nhau
- Tránh circular imports
- Lazy initialization của extensions

```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(rooms.bp)
    
    return app
```

### 2. Blueprint Pattern (Modular Routes)

**Files**: `app/routes/*.py`

**Mục đích**: Tổ chức routes theo chức năng

**Lợi ích**:
- Code modular, dễ bảo trì
- Team có thể làm việc song song
- URL prefix tự động

```python
# app/routes/rooms.py
bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@bp.route('/')
def list_rooms():
    # ...
```

### 3. Service Layer Pattern

**Files**: `app/services/*.py`

**Mục đích**: Tách business logic khỏi controllers

**Lợi ích**:
- Routes (controllers) gọn gàng, chỉ handle HTTP
- Business logic tái sử dụng được
- Dễ test logic độc lập
- Dễ thay đổi persistence layer

**Ví dụ**:
```python
# BAD: Logic trong route
@bp.route('/rooms')
def list_rooms():
    query = Room.query
    if request.args.get('search'):
        query = query.filter(Room.room_number.ilike(...))
    rooms = query.paginate(...)
    return render_template('rooms/list.html', rooms=rooms)

# GOOD: Logic trong service
@bp.route('/rooms')
def list_rooms():
    search = request.args.get('search')
    rooms = RoomService.get_all_rooms(search=search, page=1)
    return render_template('rooms/list.html', rooms=rooms)
```

### 4. Repository Pattern (Implicit via SQLAlchemy)

**Files**: `app/models.py`

**Mục đích**: Abstraction layer cho data access

**Lợi ích**:
- Tách logic database khỏi business logic
- Dễ mock trong testing
- Có thể thay database engine

```python
class Room(db.Model):
    # Model definition
    
    @staticmethod
    def get_available():
        return Room.query.filter_by(status='available').all()
```

### 5. Decorator Pattern

**Files**: `app/decorators.py`, `app/utils/helpers.py`

**Mục đích**: Extend functionality của functions

**Ví dụ**:
```python
from app.utils.helpers import requires_role

@bp.route('/admin-only')
@requires_role('admin')
def admin_view():
    # Only admin can access
```

### 6. Template Method Pattern

**Files**: `app/templates/base.html`

**Mục đích**: Define skeleton của page structure

```jinja2
<!DOCTYPE html>
<html>
<head>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 📂 Directory Structure Explained

### `/app` - Application Package

#### `/routes` - Controllers
- **Vai trò**: Handle HTTP requests/responses
- **Nhiệm vụ**:
  - Validate input (với WTForms)
  - Call service layer
  - Return templates hoặc redirects
  - Flash messages

**Quy tắc**:
- ❌ KHÔNG có business logic
- ❌ KHÔNG truy cập database trực tiếp
- ✅ CHỈ điều phối request flow

#### `/services` - Business Logic Layer
- **Vai trò**: Xử lý logic nghiệp vụ
- **Nhiệm vụ**:
  - CRUD operations
  - Business rules validation
  - Data transformation
  - Complex queries
  - Transaction management

**Quy tắc**:
- ✅ Tất cả business logic phải ở đây
- ✅ Stateless (không lưu state)
- ✅ Reusable methods
- ❌ KHÔNG import Flask request/response

#### `/models` - Data Models (ORM)
- **Vai trò**: Define database schema
- **Nhiệm vụ**:
  - Table definition
  - Relationships
  - Properties & methods liên quan data
  - Constraints

**Quy tắc**:
- ✅ SQLAlchemy models
- ✅ Có thể có helper methods
- ❌ KHÔNG có complex business logic

#### `/templates` - Jinja2 Templates
- **Vai trò**: Presentation layer
- **Cấu trúc**:
  - `base.html`: Layout chung
  - `_macros.html`: Reusable components
  - `errors/`: Error pages
  - `{module}/`: Templates theo module

#### `/static` - Static Files
- `css/`: Stylesheets
- `js/`: Client-side JavaScript
- `images/`: Images, icons

#### `/utils` - Utilities
- **helpers.py**: Helper functions (format, parse, etc.)
- **logger.py**: Logging configuration

## 🔄 Request Flow

### Ví dụ: Tạo hóa đơn mới

```
1. User submits form
   ↓
2. Route handler (invoices.py)
   - Validate form
   - Extract data
   ↓
3. Service layer (invoice_service.py)
   - Check business rules
   - Create invoice
   - Update room status
   ↓
4. Model layer (models.py)
   - SQLAlchemy ORM
   - Database transaction
   ↓
5. Database
   - Persist data
   ↓
6. Response
   - Flash message
   - Redirect to invoice list
```

**Code flow**:
```python
# 1. Route (Controller)
@bp.route('/invoices/create', methods=['POST'])
@login_required
def create_invoice():
    form = InvoiceForm()
    if form.validate_on_submit():
        data = {
            'room_id': form.room_id.data,
            'month': form.month.data,
            'year': form.year.data,
            # ...
        }
        # 2. Call service
        invoice = InvoiceService.create_invoice(data)
        flash('Tạo hóa đơn thành công', 'success')
        return redirect(url_for('invoices.view', id=invoice.id))

# 3. Service (Business Logic)
class InvoiceService:
    @staticmethod
    def create_invoice(data):
        # Validate business rules
        existing = Invoice.query.filter_by(
            room_id=data['room_id'],
            month=data['month'],
            year=data['year']
        ).first()
        
        if existing:
            raise ValueError('Hóa đơn đã tồn tại')
        
        # 4. Create model
        invoice = Invoice(**data)
        db.session.add(invoice)
        db.session.commit()
        
        return invoice
```

## 🗄️ Database Design

### Relationships

```
User (1) ─────────────── (0..1) created_by
                                   ↓
Room (1) ────────────────── (N) Tenant
  │                             
  │ (1)                         
  │                             
  └────────────────── (N) Invoice (1) ─────── (N) Payment
                            │
                            │ (N)
                            │
                          (N) InvoiceItem (N) ───── (1) Service
```

### Key Constraints

1. **Unique Constraints**:
   - `User.username`
   - `User.email`
   - `Room.room_number`
   - `Tenant.id_number`
   - `Tenant.phone`
   - `Invoice(room_id, month, year)` ⭐ Business rule

2. **Foreign Keys**:
   - `Tenant.room_id` → `Room.id`
   - `Invoice.room_id` → `Room.id`
   - `Payment.invoice_id` → `Invoice.id`

## 🔐 Security Architecture

### Authentication Flow
```
1. User submits login
   ↓
2. Validate credentials
   ↓
3. Check password hash (Werkzeug)
   ↓
4. Create session (Flask-Login)
   ↓
5. Set session cookie (encrypted)
```

### Authorization Levels
```
Admin (full access)
  │
  ├── Manager (no delete)
  │     │
  │     └── Viewer (read-only)
```

### Protection Layers
1. **CSRF Protection**: Flask-WTF
2. **SQL Injection**: SQLAlchemy ORM (parameterized queries)
3. **XSS**: Jinja2 auto-escaping
4. **Password Security**: Werkzeug password hashing
5. **Session Security**: Flask session encryption

## 📊 Error Handling Strategy

### Error Hierarchy
```
Exception (catch-all)
  ├── HTTPException
  │     ├── 400 Bad Request
  │     ├── 403 Forbidden
  │     ├── 404 Not Found
  │     └── 500 Internal Server Error
  │
  └── Custom Exceptions
        ├── ValidationError
        └── BusinessLogicError
```

### Error Flow
```
1. Exception occurs
   ↓
2. Caught by error handler
   ↓
3. Log error (with context)
   ↓
4. Rollback database transaction
   ↓
5. Return user-friendly error page
```

## 🚀 Scalability Considerations

### Current Architecture
- ✅ SQLite (development)
- ✅ Single process
- ✅ File-based sessions

### Production Recommendations
- 🔄 PostgreSQL/MySQL (multiple connections)
- 🔄 Gunicorn (multi-worker)
- 🔄 Redis (session store, caching)
- 🔄 Nginx (reverse proxy, static files)
- 🔄 Docker (containerization)

### Scaling Path
```
Phase 1 (Current): Single server
  └── SQLite + Flask dev server

Phase 2 (Small): Production single server
  └── PostgreSQL + Gunicorn + Nginx

Phase 3 (Medium): Load balancing
  ├── Multiple app servers
  ├── Shared PostgreSQL
  └── Redis cache

Phase 4 (Large): Microservices (if needed)
  ├── API service
  ├── Auth service
  ├── Payment service
  └── Report service
```

## 🧪 Testing Strategy

### Test Pyramid
```
    ╱╲
   ╱E2E╲        - Few end-to-end tests
  ╱──────╲
 ╱Integr.╲      - Some integration tests
╱──────────╲
╲   Unit   ╱    - Many unit tests
 ╲────────╱
```

### What to Test
- **Unit Tests**: Services, models, utilities
- **Integration Tests**: Routes + services + database
- **E2E Tests**: Critical user flows

## 📈 Performance Optimization

### Database
- ✅ Indexed columns
- ✅ Lazy loading
- 🔄 Query optimization
- 🔄 Connection pooling

### Caching Strategy
```
Level 1: Template fragment caching
Level 2: Query result caching (Redis)
Level 3: Page caching (Nginx)
```

### Frontend
- ✅ Minified CSS/JS
- ✅ CDN for libraries
- 🔄 Image optimization
- 🔄 Lazy loading images

## 🔄 Future Enhancements

### Planned Features
1. **REST API**: Flask-RESTFUL for mobile app
2. **WebSocket**: Real-time notifications
3. **Email**: Invoice reminders, alerts
4. **Export**: PDF invoices, Excel reports
5. **Backup**: Automated database backups
6. **Multi-tenancy**: Support nhiều nhà trọ

### Architecture Evolution
```
Current: Monolithic
  ↓
Next: Modular monolith with API
  ↓
Future: Microservices (if scale requires)
```

---

**Nguyên tắc thiết kế**: KISS (Keep It Simple, Stupid) + SOLID + DRY

Kiến trúc này cân bằng giữa **simplicity** (dễ hiểu, dễ bảo trì) và **scalability** (có thể mở rộng khi cần).
