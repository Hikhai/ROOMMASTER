# BÁO CÁO ĐỀ TÀI MÔN PHẦN MỀM MÃ NGUỒN MỞ

**Họ và tên:** Hồ Hữu Khải  
**Mã sinh viên:** 21T1020436  
**Ngày hoàn thành:** 08/11/2025

---

## 1. Tên đề tài

**Hệ thống quản lý phòng trọ RoomMaster bằng Flask**

---

## 2. Bối cảnh và vấn đề thực tế

### Bối cảnh
Việc quản lý phòng trọ cho thuê hiện nay phần lớn vẫn được thực hiện thủ công hoặc sử dụng sổ sách, bảng tính Excel. Điều này gây khó khăn trong việc theo dõi tình trạng phòng, quản lý khách thuê, tính toán hóa đơn tiền phòng, dịch vụ hàng tháng và theo dõi công nợ.

### Vấn đề
- **Ai gặp vấn đề:** Chủ nhà trọ, quản lý nhà trọ, người quản lý nhiều căn phòng cho thuê
- **Vấn đề cụ thể:**
  - Khó khăn trong việc theo dõi trạng thái phòng (trống/đã thuê)
  - Tính toán hóa đơn thủ công mất thời gian và dễ sai sót
  - Không có hệ thống theo dõi lịch sử thanh toán
  - Khó tạo báo cáo doanh thu và công nợ
  - Không có phân quyền rõ ràng khi có nhiều người quản lý

### Tại sao cần xây dựng
- Tự động hóa quy trình quản lý phòng trọ
- Giảm thiểu sai sót trong tính toán và theo dõi
- Tăng tính chuyên nghiệp trong quản lý
- Dễ dàng tra cứu thông tin và tạo báo cáo

### Hệ thống tương tự và điểm khác biệt
Có một số phần mềm quản lý phòng trọ trên thị trường (Phần mềm quản lý nhà trọ, Motel Room Manager), tuy nhiên:
- **Điểm khác biệt của RoomMaster:**
  - Mã nguồn mở, miễn phí
  - Giao diện đơn giản, dễ sử dụng
  - Kiến trúc rõ ràng với Service Layer, dễ mở rộng
  - Hỗ trợ phân quyền người dùng (admin, manager, viewer)
  - Tạo hóa đơn hàng loạt tự động cho tất cả phòng
  - Báo cáo chi tiết về doanh thu, công nợ, tỷ lệ lấp đầy

---

## 3. Mục tiêu và phạm vi của ứng dụng

### Mục tiêu
- Xây dựng hệ thống quản lý phòng trọ hoàn chỉnh với đầy đủ chức năng CRUD
- Tự động hóa việc tạo hóa đơn và tính toán tiền phòng, dịch vụ
- Cung cấp báo cáo trực quan về tình hình kinh doanh
- Phân quyền rõ ràng cho các loại người dùng

### Kết quả cụ thể
- Người dùng có thể quản lý thông tin phòng, khách thuê một cách dễ dàng
- Tự động tạo hóa đơn hàng tháng cho tất cả phòng đang cho thuê
- Theo dõi lịch sử thanh toán chi tiết
- Xem báo cáo doanh thu, công nợ, tỷ lệ lấp đầy theo thời gian

### Phạm vi
- **Hoàn chỉnh:** Ứng dụng web đầy đủ chức năng với giao diện responsive
- **Có đăng nhập:** Hệ thống authentication và phân quyền
- **Database:** SQLite cho development, có thể chuyển sang PostgreSQL
- **Deployment:** Chạy được trên localhost và có thể deploy lên hosting
- **Không có:** Mobile app riêng, tích hợp thanh toán online

---

## 4. Phân tích người dùng

### Các loại người dùng

#### 4.1. Admin (Quản trị viên)
- **Quyền hạn:** Toàn quyền truy cập và quản lý hệ thống
- **Hành vi:**
  - Quản lý tài khoản người dùng (thêm, sửa, xóa)
  - Cấu hình hệ thống, dịch vụ
  - Xem tất cả báo cáo
  - Quản lý toàn bộ phòng, khách thuê, hóa đơn

#### 4.2. Manager (Người quản lý)
- **Quyền hạn:** Quản lý phòng, khách thuê, hóa đơn
- **Hành vi:**
  - Thêm/sửa/xóa phòng và khách thuê
  - Tạo hóa đơn (đơn lẻ và hàng loạt)
  - Ghi nhận thanh toán
  - Xem báo cáo
  - Không được quản lý người dùng

#### 4.3. Viewer (Người xem)
- **Quyền hạn:** Chỉ xem thông tin
- **Hành vi:**
  - Xem danh sách phòng, khách thuê
  - Xem hóa đơn và lịch sử thanh toán
  - Xem báo cáo
  - Không được thêm/sửa/xóa bất kỳ dữ liệu nào

---

## 5. Các chức năng chính

### Chức năng bắt buộc (phiên bản đầu tiên)

1. **Đăng nhập và phân quyền**
   - Đăng nhập với username/password
   - Phân quyền theo role (admin, manager, viewer)
   - Đăng xuất

2. **Quản lý phòng (CRUD)**
   - Thêm phòng mới với thông tin: số phòng, diện tích, giá thuê
   - Xem danh sách phòng và trạng thái (trống/đã thuê)
   - Sửa thông tin phòng
   - Xóa phòng (nếu chưa có khách)
   - Xem chi tiết phòng và lịch sử khách thuê

3. **Quản lý khách thuê (CRUD)**
   - Thêm khách thuê mới
   - Gán khách vào phòng (check-in)
   - Xem danh sách khách thuê
   - Sửa thông tin khách
   - Checkout khách (kết thúc hợp đồng)
   - Xem lịch sử hóa đơn của khách

4. **Quản lý hóa đơn**
   - Tạo hóa đơn đơn lẻ cho một phòng
   - Tạo hóa đơn hàng loạt cho tất cả phòng đang cho thuê
   - Xem danh sách hóa đơn với trạng thái (chưa thanh toán/đã thanh toán/thanh toán một phần)
   - Ghi nhận thanh toán (toàn bộ hoặc một phần)
   - Xem chi tiết hóa đơn và lịch sử thanh toán

5. **Báo cáo và thống kê**
   - Báo cáo doanh thu theo tháng/năm
   - Báo cáo công nợ (các hóa đơn chưa thanh toán)
   - Báo cáo tỷ lệ lấp đầy phòng
   - Báo cáo danh sách khách thuê hiện tại

### Chức năng bổ sung (đã hoàn thiện)

6. **Quản lý dịch vụ** (Admin only)
   - ✅ Thêm/sửa/xóa các loại dịch vụ (điện, nước, internet, vệ sinh...)
   - ✅ Cấu hình giá dịch vụ và đơn vị
   - ✅ Bật/Tắt dịch vụ (soft delete)
   - ✅ Gợi ý dịch vụ phổ biến khi tạo mới

7. **Quản lý người dùng** (Admin only)
   - ✅ Thêm/sửa/xóa tài khoản người dùng
   - ✅ Phân quyền cho người dùng (admin/manager/viewer)
   - ✅ Hiển thị role badge trên navbar

8. **Giao diện nâng cao**
   - ✅ Dark Mode với localStorage persistence
   - ✅ Clickable table rows
   - ✅ Modern footer cố định
   - ✅ Toast notifications
   - ✅ Smooth scroll to top button

---

## 6. Giao diện và trải nghiệm người dùng (UI/UX)

### Công nghệ giao diện
- **Framework:** Bootstrap 5.3.0
- **Icons:** Bootstrap Icons 1.11.0
- **Template engine:** Jinja2
- **Dark Mode:** Hỗ trợ chế độ sáng/tối với CSS variables và localStorage
- **Responsive:** Hoàn toàn tương thích desktop, tablet, mobile
- **JavaScript:** Vanilla JS cho theme toggle, clickable rows, smooth scroll

### Tính năng UI nổi bật

#### Dark Mode
- Toggle button trên navbar (icon mặt trời/mặt trăng)
- Lưu preference vào localStorage
- Tự động load theme khi mở lại trang
- CSS variables tự động thay đổi màu sắc
- Footer gradient đẹp mắt cho cả 2 chế độ

#### Navbar Active State
- Tự động highlight menu đang active dựa vào `request.endpoint`
- Màu khác biệt rõ ràng giữa active và inactive

#### Clickable Table Rows
- Click vào bất kỳ hàng nào trong bảng để xem chi tiết
- Cursor pointer khi hover
- Smooth transition

#### Modern Footer
- Fixed ở dưới cùng với flexbox
- 3 cột: Logo/Info | Contact | Social Links
- Responsive collapse trên mobile
- Links: Privacy Policy, Terms of Service

### Quy trình thao tác chính

#### Quy trình quản lý phòng và khách thuê:
```
Đăng nhập → Dashboard → 
├─ Quản lý phòng → Thêm/Sửa/Xem phòng
├─ Quản lý khách → Thêm khách → Gán vào phòng
└─ Xem danh sách phòng đã cho thuê
```

#### Quy trình tạo hóa đơn:
```
Đăng nhập → Hóa đơn → 
├─ Tạo hóa đơn đơn lẻ → Chọn phòng → Nhập dịch vụ → Lưu
└─ Tạo hóa đơn hàng loạt → Chọn tháng/năm → Tự động tạo cho tất cả phòng
```

#### Quy trình thanh toán:
```
Danh sách hóa đơn → Chọn hóa đơn chưa thanh toán → 
Nhập số tiền thanh toán → Ghi nhận → Cập nhật trạng thái
```

#### Quy trình quản lý dịch vụ (Admin):
```
Menu Dịch vụ (chỉ Admin thấy) →
├─ Thêm dịch vụ mới (Điện, Nước, Internet...)
├─ Sửa giá dịch vụ
└─ Bật/Tắt dịch vụ (soft delete)
```

### Mô tả giao diện chính

**Dashboard:**
- Hiển thị thống kê tổng quan: số phòng, số phòng đã cho thuê, doanh thu tháng, công nợ
- Cards với màu sắc khác nhau (primary, success, warning, danger)
- Navbar với theme toggle và user dropdown
- Footer cố định ở dưới

**Danh sách (List views):**
- Bảng dữ liệu responsive
- Nút action (Xem/Sửa/Xóa) rõ ràng
- Click vào hàng để xem chi tiết
- Status badges (Đã thanh toán: success, Chưa thanh toán: danger)
- Toast notifications khi thao tác thành công

**Form tạo/sửa:**
- Form rõ ràng với validation
- Hiển thị lỗi cụ thể nếu có
- Nút Save/Cancel
- Date picker cho ngày tháng
- Gợi ý dịch vụ phổ biến (trong trang tạo dịch vụ)

---

## 7. Công nghệ mã nguồn mở sử dụng

### Ngôn ngữ lập trình
- **Python 3.14.0**

### Framework / Thư viện chính
- **Flask 3.0.0** - Web framework chính
- **Flask-SQLAlchemy 3.1.1** - ORM cho database
- **Flask-Login 0.6.3** - Quản lý authentication và session
- **Flask-WTF 1.2.1** - Form validation
- **Flask-Migrate 4.0.5** - Database migration tool
- **WTForms 3.1.1** - Form handling và validation

### Cơ sở dữ liệu
- **SQLite** (built-in Python) - Development database
- **SQLAlchemy** - ORM layer

### Thư viện giao diện
- **Bootstrap 5.3.0** - CSS framework responsive
- **Bootstrap Icons 1.11.0** - Icon library
- **Flatpickr** - Date picker cho form

### Thư viện bảo mật
- **Werkzeug 3.0.1** - Password hashing (PBKDF2)
- **Flask-Login** - Session management

### Công cụ development
- **python-dotenv** - Quản lý environment variables
- **Git** - Version control
- **pip** - Package manager
- **venv** - Virtual environment

---

## 8. Cấu trúc dữ liệu (sơ bộ)

### Các bảng dữ liệu chính

#### 8.1. Bảng `users`
- **Mục đích:** Lưu thông tin người dùng hệ thống
- **Các trường:**
  - `id` (khóa chính)
  - `username` (unique)
  - `password_hash`
  - `full_name`
  - `role` (admin/manager/viewer)
  - `created_at`

#### 8.2. Bảng `rooms`
- **Mục đích:** Lưu thông tin phòng cho thuê
- **Các trường:**
  - `id` (khóa chính)
  - `room_number` (unique)
  - `area` (diện tích m²)
  - `price` (giá thuê cơ bản)
  - `status` (available/occupied)
  - `description`
  - `created_at`

#### 8.3. Bảng `tenants`
- **Mục đích:** Lưu thông tin khách thuê
- **Các trường:**
  - `id` (khóa chính)
  - `full_name`
  - `phone`
  - `email`
  - `id_number` (CCCD/CMND)
  - `room_id` (khóa ngoại → rooms)
  - `check_in_date`
  - `check_out_date` (null nếu đang thuê)
  - `deposit` (tiền đặt cọc)
  - `notes`
  - `created_at`

#### 8.4. Bảng `services`
- **Mục đích:** Lưu các loại dịch vụ (điện, nước, internet...)
- **Các trường:**
  - `id` (khóa chính)
  - `name` (unique)
  - `unit` (kWh, m³, tháng...)
  - `price` (đơn giá)
  - `description`
  - `is_active` (True/False)
  - `created_at`

#### 8.5. Bảng `invoices`
- **Mục đích:** Lưu hóa đơn hàng tháng
- **Các trường:**
  - `id` (khóa chính)
  - `room_id` (khóa ngoại → rooms)
  - `tenant_id` (khóa ngoại → tenants)
  - `month`
  - `year`
  - `room_price` (giá phòng trong tháng đó)
  - `total_amount` (tổng tiền)
  - `paid_amount` (số tiền đã thanh toán)
  - `status` (unpaid/partial/paid)
  - `due_date`
  - `notes`
  - `created_at`
  - **Unique constraint:** (room_id, month, year)

#### 8.6. Bảng `invoice_services`
- **Mục đích:** Chi tiết dịch vụ trong mỗi hóa đơn
- **Các trường:**
  - `id` (khóa chính)
  - `invoice_id` (khóa ngoại → invoices)
  - `service_id` (khóa ngoại → services)
  - `quantity` (số lượng sử dụng)
  - `unit_price` (đơn giá tại thời điểm đó)
  - `amount` (thành tiền)

#### 8.7. Bảng `payments`
- **Mục đích:** Lưu lịch sử thanh toán
- **Các trường:**
  - `id` (khóa chính)
  - `invoice_id` (khóa ngoại → invoices)
  - `amount` (số tiền thanh toán)
  - `payment_date`
  - `payment_method` (cash/transfer/...)
  - `notes`
  - `created_by` (user_id)

### Mối quan hệ giữa các bảng

- **users ↔ rooms/tenants/invoices:** Không có quan hệ trực tiếp (chỉ log actions)
- **rooms ↔ tenants:** 1-n (một phòng có nhiều khách thuê theo thời gian)
- **rooms ↔ invoices:** 1-n (một phòng có nhiều hóa đơn)
- **tenants ↔ invoices:** 1-n (một khách có nhiều hóa đơn)
- **invoices ↔ invoice_services:** 1-n (một hóa đơn có nhiều dịch vụ)
- **invoices ↔ payments:** 1-n (một hóa đơn có nhiều lần thanh toán)
- **services ↔ invoice_services:** 1-n (một dịch vụ xuất hiện trong nhiều hóa đơn)

---

## 9. Kết quả đã hoàn thành

### Trạng thái dự án: ✅ HOÀN THIỆN 100%

| Giai đoạn | Nội dung công việc | Trạng thái |
|-----------|-------------------|-----------|
| **Tuần 1–2** | **Phân tích và thiết kế**<br>- Thiết kế database schema<br>- Thiết kế kiến trúc MVC + Service Layer<br>- Setup project structure | ✅ Hoàn thành |
| **Tuần 3–4** | **Xây dựng chức năng cơ bản**<br>- Implement models và database<br>- Xây dựng authentication<br>- CRUD cho rooms và tenants<br>- Tạo giao diện cơ bản | ✅ Hoàn thành |
| **Tuần 5–6** | **Chức năng nâng cao**<br>- Quản lý hóa đơn và thanh toán<br>- Tạo hóa đơn hàng loạt<br>- Lịch sử thanh toán<br>- Phân quyền người dùng | ✅ Hoàn thành |
| **Tuần 7–8** | **Báo cáo và hoàn thiện**<br>- Xây dựng các trang báo cáo<br>- Hoàn thiện giao diện<br>- Dark mode và UI improvements<br>- Testing và fix bugs | ✅ Hoàn thành |
| **Tuần 9** | **Chức năng mở rộng**<br>- Quản lý dịch vụ (Admin)<br>- Modern footer<br>- Viết tài liệu hướng dẫn<br>- Code documentation | ✅ Hoàn thành |

---

## 10. Kết quả đạt được

### Môi trường chạy
- ✅ **Localhost:** Chạy hoàn hảo trên http://127.0.0.1:5000
- ✅ **Database:** SQLite với 10 phòng, 6 khách thuê, 5 dịch vụ mẫu
- ✅ **Seed data:** Script tạo dữ liệu mẫu tự động

### Tài khoản demo
```
Admin:     admin / admin123
Manager:   manager / manager123  
Viewer:    viewer / viewer123
```

### Tính năng đã triển khai (100%)

#### ✅ Authentication & Authorization
- Đăng nhập/đăng xuất với Flask-Login
- Phân quyền 3 cấp: Admin, Manager, Viewer
- Decorators: @login_required, @admin_required, @manager_required
- Session management an toàn

#### ✅ Quản lý phòng trọ
- CRUD đầy đủ (Create, Read, Update, Delete)
- Trạng thái: Available, Occupied, Maintenance
- Tự động cập nhật status khi có khách check-in/out
- Xem lịch sử khách thuê theo phòng

#### ✅ Quản lý khách thuê
- Thêm khách với thông tin đầy đủ (CCCD, SĐT, Email)
- Check-in/Check-out tự động cập nhật phòng
- Quản lý tiền cọc
- Xem lịch sử hóa đơn của khách

#### ✅ Quản lý hóa đơn
- Tạo hóa đơn đơn lẻ cho từng phòng
- **Tạo hóa đơn hàng loạt** cho tất cả phòng
- Unique constraint: 1 phòng - 1 tháng - 1 hóa đơn
- Tính toán tự động: Tiền phòng + Điện + Nước + Phí khác
- Trạng thái: Unpaid, Partial, Paid

#### ✅ Quản lý thanh toán
- Thanh toán từng phần (partial payment)
- Nhiều phương thức: Tiền mặt, Chuyển khoản, Ví điện tử
- Lịch sử thanh toán chi tiết
- Tự động cập nhật status hóa đơn
- Xóa thanh toán (rollback)

#### ✅ Báo cáo & Thống kê
- Báo cáo doanh thu theo tháng/năm
- Báo cáo tỷ lệ lấp đầy phòng
- Báo cáo hóa đơn quá hạn
- Báo cáo khách thuê hiện tại
- Dashboard với số liệu tổng quan

#### ✅ Quản lý dịch vụ (Admin only)
- CRUD đầy đủ cho dịch vụ
- Bật/Tắt dịch vụ (soft delete)
- Gợi ý dịch vụ phổ biến
- Validation: Tên unique, giá không âm

#### ✅ Quản lý người dùng (Admin only)
- CRUD tài khoản người dùng
- Phân quyền admin/manager/viewer
- Hiển thị role badge

#### ✅ Giao diện nâng cao
- **Dark Mode**: Toggle với localStorage persistence
- **Responsive**: Desktop, Tablet, Mobile
- **Clickable rows**: Click vào hàng để xem chi tiết
- **Modern footer**: Cố định dưới cùng, tương thích theme
- **Navbar active state**: Tự động highlight
- **Toast notifications**: Thông báo đẹp mắt
- **Smooth scroll**: Nút scroll to top

### Kiến trúc code

```
app/
├── __init__.py              # App factory với error handlers
├── models.py                # 7 models: User, Room, Tenant, Invoice, Payment, Service
├── forms.py                 # WTForms cho validation
├── decorators.py            # @admin_required, @manager_required
├── errors.py                # Error handlers 403, 404, 500
├── routes/                  # 7 blueprints
│   ├── auth.py              # Authentication
│   ├── main.py              # Dashboard
│   ├── rooms.py             # Quản lý phòng
│   ├── tenants.py           # Quản lý khách
│   ├── invoices.py          # Quản lý hóa đơn
│   ├── reports.py           # Báo cáo
│   ├── services.py          # Quản lý dịch vụ
│   └── users.py             # Quản lý người dùng
├── services/                # Business Logic Layer
│   ├── room_service.py      # Logic nghiệp vụ phòng
│   ├── tenant_service.py    # Logic nghiệp vụ khách
│   ├── invoice_service.py   # Logic nghiệp vụ hóa đơn
│   ├── payment_service.py   # Logic nghiệp vụ thanh toán
│   └── report_service.py    # Logic báo cáo
├── utils/                   # Utilities
│   ├── helpers.py           # Helper functions
│   └── logger.py            # Logging configuration
├── templates/               # 30+ Jinja2 templates
└── static/
    ├── css/style.css        # 1000+ lines CSS với dark mode
    └── js/main.js           # Theme toggle, clickable rows
```

### Tài liệu kỹ thuật

- ✅ **README.md**: Hướng dẫn cài đặt và chạy dự án
- ✅ **GUIDE.md**: Hướng dẫn sử dụng chi tiết cho người dùng
- ✅ **SERVICES_GUIDE.md**: Hướng dẫn quản lý dịch vụ
- ✅ **WORKFLOW.md**: Luồng hoạt động chi tiết của code
- ✅ **requirements.txt**: Danh sách dependencies đầy đủ
- ✅ **seed_data.py**: Script tạo dữ liệu mẫu

### Số liệu thống kê code

- **Tổng files Python**: 25+ files
- **Tổng templates**: 30+ HTML files
- **Lines of Code**: ~3000+ lines Python, ~1000+ lines CSS, ~200+ lines JavaScript
- **Models**: 7 models với relationships đầy đủ
- **Routes**: 50+ endpoints
- **Services**: 5 service layers

### Đã test các tình huống

✅ Đăng nhập với 3 role khác nhau  
✅ Phân quyền truy cập các trang  
✅ Thêm/sửa/xóa phòng và khách thuê  
✅ Tạo hóa đơn đơn lẻ và hàng loạt  
✅ Thanh toán từng phần và toàn bộ  
✅ Xem các báo cáo  
✅ Quản lý dịch vụ (admin)  
✅ Dark mode toggle và persistence  
✅ Responsive trên nhiều kích thước màn hình  
✅ Error handling (404, 403, 500)  

---

## 11. Cam kết

Tôi, **Hồ Hữu Khải**, cam kết:

- ✅ Dự án RoomMaster được phát triển hoàn toàn bởi cá nhân, không sao chép mã nguồn
- ✅ Toàn bộ code được viết và hiểu rõ từng dòng, từng chức năng
- ✅ Có tham khảo tài liệu chính thức: Flask Documentation, Bootstrap Documentation, SQLAlchemy Documentation
- ✅ Tôi có thể giải thích và demo bất kỳ phần nào trong dự án
- ✅ Dự án đã hoàn thành 100% các chức năng đề ra và thêm nhiều tính năng nâng cao
- ✅ Code được tổ chức theo kiến trúc MVC + Service Layer, dễ bảo trì và mở rộng
- ✅ Có đầy đủ tài liệu kỹ thuật và hướng dẫn sử dụng

**Ký tên:** Hồ Hữu Khải

**Ngày hoàn thành:** 08/11/2025

---

## Phụ lục: Cấu trúc thư mục dự án (Đã triển khai)

```
RoomMaster/
├── app/
│   ├── __init__.py           # App factory với error handlers
│   ├── models.py             # 7 Database models
│   ├── forms.py              # WTForms cho validation
│   ├── decorators.py         # Custom decorators (@admin_required, @manager_required)
│   ├── errors.py             # Error handlers (403, 404, 500)
│   │
│   ├── routes/               # Blueprints (Controllers)
│   │   ├── auth.py           # Đăng nhập/đăng xuất
│   │   ├── main.py           # Dashboard
│   │   ├── rooms.py          # Quản lý phòng
│   │   ├── tenants.py        # Quản lý khách thuê
│   │   ├── invoices.py       # Quản lý hóa đơn
│   │   ├── reports.py        # Báo cáo thống kê
│   │   ├── services.py       # Quản lý dịch vụ (Admin)
│   │   └── users.py          # Quản lý người dùng (Admin)
│   │
│   ├── services/             # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── room_service.py      # Logic nghiệp vụ phòng
│   │   ├── tenant_service.py    # Logic nghiệp vụ khách thuê
│   │   ├── invoice_service.py   # Logic nghiệp vụ hóa đơn
│   │   ├── payment_service.py   # Logic nghiệp vụ thanh toán
│   │   └── report_service.py    # Logic báo cáo
│   │
│   ├── utils/                # Utilities & Helpers
│   │   ├── __init__.py
│   │   ├── helpers.py           # Helper functions
│   │   └── logger.py            # Logging configuration
│   │
│   ├── templates/            # Jinja2 templates (30+ files)
│   │   ├── base.html            # Base template với navbar, footer
│   │   ├── dashboard.html       # Trang chủ
│   │   ├── _macros.html         # Template macros
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── rooms/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   ├── tenants/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── add.html
│   │   │   └── edit.html
│   │   ├── invoices/
│   │   │   ├── list.html
│   │   │   ├── view.html
│   │   │   ├── create.html
│   │   │   ├── create_bulk.html
│   │   │   ├── edit.html
│   │   │   └── payment.html
│   │   ├── reports/
│   │   │   ├── index.html
│   │   │   ├── revenue.html
│   │   │   ├── occupancy.html
│   │   │   ├── overdue.html
│   │   │   └── tenants.html
│   │   ├── services/
│   │   │   ├── list.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   ├── users/
│   │   │   ├── list.html
│   │   │   ├── add.html
│   │   │   └── edit.html
│   │   └── errors/              # Error pages
│   │       ├── 403.html
│   │       ├── 404.html
│   │       └── 500.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Custom styles (1000+ lines)
│       └── js/
│           └── main.js          # JavaScript utilities
│
├── logs/                     # Log files
│   └── roommaster.log
├── config.py                 # Configuration
├── requirements.txt          # Dependencies (15 packages)
├── run.py                    # Entry point
├── seed_data.py              # Sample data generator
├── migrate_db.py             # Database migration script
├── roommaster.db             # SQLite database
│
├── README.md                 # Hướng dẫn cài đặt và chạy
├── GUIDE.md                  # Hướng dẫn sử dụng chi tiết
├── SERVICES_GUIDE.md         # Hướng dẫn quản lý dịch vụ
├── WORKFLOW.md               # Luồng hoạt động chi tiết code
└── HoHuuKhai_21T1020436.md   # Báo cáo đề tài (file này)
```

---

## Liên kết tài liệu

- 📖 **README.md**: Hướng dẫn cài đặt, chạy dự án, và tính năng tổng quan
- 📚 **GUIDE.md**: Hướng dẫn sử dụng từng chức năng chi tiết
- ⚙️ **SERVICES_GUIDE.md**: Hướng dẫn quản lý dịch vụ cho Admin
- 🔄 **WORKFLOW.md**: Luồng hoạt động chi tiết của code, kiến trúc, và business logic

---

**HẾT**
