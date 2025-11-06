# Hệ Thống Phân Quyền - RoomMaster

## Các Role và Quyền Hạn

### 1. 👑 ADMIN (Quản trị viên)
**Quyền cao nhất - Quản lý toàn hệ thống**

#### Được phép:
- ✅ Tất cả quyền của Manager
- ✅ **Quản lý nhân viên** (Users)
  - Thêm nhân viên mới
  - Sửa thông tin nhân viên
  - Xóa nhân viên
  - Thay đổi role
- ✅ **Xóa dữ liệu quan trọng**
  - Xóa phòng
  - Xóa khách thuê
  - Xóa hóa đơn (chỉ hóa đơn chưa thanh toán)

#### Menu hiển thị:
- Dashboard
- Phòng (+ nút Thêm phòng, Edit, Delete)
- Khách thuê (+ nút Thêm, Edit, Checkout, Delete)
- Hóa đơn (+ nút Tạo mới, Tạo hàng loạt, Edit, Thanh toán)
- Báo cáo
- **Nhân viên** (chỉ Admin)

---

### 2. 📋 MANAGER (Quản lý)
**Quản lý vận hành hàng ngày**

#### Được phép:
- ✅ **Xem tất cả dữ liệu**
- ✅ **Quản lý phòng**
  - Thêm phòng mới
  - Sửa thông tin phòng
  - Thay đổi trạng thái phòng
- ✅ **Quản lý khách thuê**
  - Thêm khách thuê mới
  - Sửa thông tin khách
  - Đánh dấu chuyển đi
- ✅ **Quản lý hóa đơn**
  - Tạo hóa đơn đơn lẻ
  - Tạo hóa đơn hàng loạt
  - Sửa hóa đơn (chưa thanh toán)
  - Ghi nhận thanh toán
- ✅ **Xem báo cáo**

#### Không được phép:
- ❌ Quản lý nhân viên
- ❌ Xóa phòng
- ❌ Xóa khách thuê
- ❌ Xóa hóa đơn

#### Menu hiển thị:
- Dashboard (+ nút Thêm phòng, Thêm khách, Tạo hóa đơn)
- Phòng (+ nút Thêm, Edit | ❌ Delete)
- Khách thuê (+ nút Thêm, Edit, Checkout | ❌ Delete)
- Hóa đơn (+ nút Tạo mới, Tạo hàng loạt, Edit, Thanh toán)
- Báo cáo

---

### 3. 👀 VIEWER (Chỉ xem)
**Chỉ được xem dữ liệu, không thay đổi**

#### Được phép:
- ✅ Xem Dashboard
- ✅ Xem danh sách phòng
- ✅ Xem chi tiết phòng
- ✅ Xem danh sách khách thuê
- ✅ Xem chi tiết khách thuê
- ✅ Xem danh sách hóa đơn
- ✅ Xem chi tiết hóa đơn
- ✅ Xem báo cáo

#### Không được phép:
- ❌ Thêm/Sửa/Xóa bất kỳ dữ liệu nào
- ❌ Tạo hóa đơn
- ❌ Ghi nhận thanh toán
- ❌ Thay đổi trạng thái phòng/khách

#### Menu hiển thị:
- Dashboard (❌ Không có nút Thao tác nhanh)
- Phòng (❌ Không có nút Thêm/Edit/Delete)
- Khách thuê (❌ Không có nút Thêm/Edit/Checkout/Delete)
- Hóa đơn (❌ Không có nút Tạo/Edit/Thanh toán)
- Báo cáo

---

## Chi Tiết Phân Quyền Theo Chức Năng

### Phòng (Rooms)
| Chức năng | Admin | Manager | Viewer |
|-----------|-------|---------|--------|
| Xem danh sách | ✅ | ✅ | ✅ |
| Xem chi tiết | ✅ | ✅ | ✅ |
| Thêm phòng | ✅ | ✅ | ❌ |
| Sửa phòng | ✅ | ✅ | ❌ |
| Xóa phòng | ✅ | ❌ | ❌ |

### Khách thuê (Tenants)
| Chức năng | Admin | Manager | Viewer |
|-----------|-------|---------|--------|
| Xem danh sách | ✅ | ✅ | ✅ |
| Xem chi tiết | ✅ | ✅ | ✅ |
| Thêm khách | ✅ | ✅ | ❌ |
| Sửa thông tin | ✅ | ✅ | ❌ |
| Đánh dấu chuyển đi | ✅ | ✅ | ❌ |
| Xóa khách | ✅ | ❌ | ❌ |

### Hóa đơn (Invoices)
| Chức năng | Admin | Manager | Viewer |
|-----------|-------|---------|--------|
| Xem danh sách | ✅ | ✅ | ✅ |
| Xem chi tiết | ✅ | ✅ | ✅ |
| Tạo hóa đơn | ✅ | ✅ | ❌ |
| Tạo hàng loạt | ✅ | ✅ | ❌ |
| Sửa hóa đơn | ✅ | ✅ | ❌ |
| Ghi nhận thanh toán | ✅ | ✅ | ❌ |
| Xóa hóa đơn | ✅ | ❌ | ❌ |

### Báo cáo (Reports)
| Chức năng | Admin | Manager | Viewer |
|-----------|-------|---------|--------|
| Doanh thu | ✅ | ✅ | ✅ |
| Công suất | ✅ | ✅ | ✅ |
| Khách thuê | ✅ | ✅ | ✅ |
| Quá hạn | ✅ | ✅ | ✅ |

### Nhân viên (Users)
| Chức năng | Admin | Manager | Viewer |
|-----------|-------|---------|--------|
| Xem danh sách | ✅ | ❌ | ❌ |
| Thêm nhân viên | ✅ | ❌ | ❌ |
| Sửa nhân viên | ✅ | ❌ | ❌ |
| Xóa nhân viên | ✅ | ❌ | ❌ |

---

## Cách Kiểm Tra Quyền Trong Template

### Sử dụng Jinja2 Condition:

```jinja2
{# Chỉ Admin #}
{% if current_user.role == 'admin' %}
    <button>Xóa</button>
{% endif %}

{# Admin hoặc Manager #}
{% if current_user.role in ['admin', 'manager'] %}
    <button>Sửa</button>
{% endif %}

{# Viewer không thấy gì #}
{% if current_user.role in ['admin', 'manager'] %}
    <a href="{{ url_for('rooms.add_room') }}" class="btn btn-primary">
        Thêm phòng
    </a>
{% endif %}
```

---

## Cách Kiểm Tra Quyền Trong Routes (Backend)

### Sử dụng Decorators:

```python
from app.decorators import admin_required, manager_or_admin

# Chỉ Admin
@bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    # ...
    pass

# Admin hoặc Manager
@bp.route('/create', methods=['GET', 'POST'])
@manager_or_admin
def create_invoice():
    # ...
    pass
```

---

## Tài Khoản Mặc Định

Sau khi chạy `seed_data.py`:

| Username | Password | Role | Mô tả |
|----------|----------|------|-------|
| admin | admin123 | admin | Tài khoản quản trị viên |
| manager | manager123 | manager | Tài khoản quản lý |
| viewer | viewer123 | viewer | Tài khoản chỉ xem |

---

## Lưu Ý Bảo Mật

1. ✅ **Backend protection**: Tất cả routes đều có decorator kiểm tra quyền
2. ✅ **Frontend hiding**: Nút/link sẽ ẩn nếu không có quyền
3. ✅ **Kết hợp 2 lớp**: Ngay cả khi bypass frontend, backend vẫn chặn
4. ✅ **Flash message**: Hiển thị thông báo rõ ràng khi không có quyền
5. ✅ **HTTP 403**: Trả về Forbidden nếu cố truy cập không hợp lệ

---

## Cập Nhật Log

**Ngày 05/11/2025**
- ✅ Đã ẩn tất cả nút thêm/sửa/xóa với Viewer
- ✅ Đã ẩn nút xóa với Manager
- ✅ Đã ẩn menu Nhân viên với Manager/Viewer
- ✅ Dashboard: Ẩn "Thao tác nhanh" với Viewer
- ✅ Tất cả danh sách: Ẩn nút action theo role
- ✅ Trang chi tiết: Ẩn nút sửa/xóa theo role
- ✅ Hóa đơn: Ẩn nút thanh toán với Viewer

---

**🎯 Mục tiêu**: Hệ thống phân quyền rõ ràng, an toàn, dễ mở rộng
