# BÁO CÁO ĐỀ TÀI MÔN PHẦN MỀM MÃ NGUỒN MỞ

**Họ và tên:** Hồ Hữu Khải  
**Mã sinh viên:** 21T1020436  
**Ngày:** 07/11/2025

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

### Chức năng bổ sung (có thể mở rộng sau)

6. **Quản lý dịch vụ**
   - Thêm/sửa/xóa các loại dịch vụ (điện, nước, internet, vệ sinh...)
   - Cấu hình giá dịch vụ

7. **Quản lý người dùng** (chỉ admin)
   - Thêm/sửa/xóa tài khoản người dùng
   - Phân quyền cho người dùng

---

## 6. Giao diện và trải nghiệm người dùng (UI/UX)

### Công nghệ giao diện
- **Framework:** Bootstrap 5
- **Responsive:** Có, tương thích với desktop và tablet
- **Template engine:** Jinja2
- **Thiết kế:** Giao diện sạch sẽ, dễ sử dụng với sidebar navigation

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

### Mô tả giao diện chính

**Dashboard:**
- Hiển thị thống kê tổng quan: số phòng, số phòng đã cho thuê, doanh thu tháng, công nợ
- Menu sidebar với các chức năng chính
- Responsive với màu sắc chuyên nghiệp

**Danh sách (List views):**
- Bảng dữ liệu với pagination
- Nút action (Xem/Sửa/Xóa) rõ ràng
- Có filter và search (sẽ bổ sung)
- Click vào hàng để xem chi tiết

**Form tạo/sửa:**
- Form rõ ràng với validation
- Hiển thị lỗi cụ thể nếu có
- Nút Save/Cancel

---

## 7. Công nghệ mã nguồn mở dự kiến sử dụng

### Ngôn ngữ lập trình
- **Python 3.10+**

### Framework / Thư viện chính
- **Flask** - Web framework chính
- **Flask-SQLAlchemy** - ORM cho database
- **Flask-Login** - Quản lý authentication
- **Flask-WTF** - Form validation
- **Flask-Migrate** - Database migration

### Cơ sở dữ liệu
- **Development:** SQLite
- **Production (tùy chọn):** PostgreSQL

### Thư viện giao diện
- **Bootstrap 5** - CSS framework
- **Font Awesome** - Icons
- **jQuery** - JavaScript utilities (tối thiểu)

### Thư viện khác
- **python-dotenv** - Quản lý environment variables
- **Werkzeug** - Password hashing
- **Jinja2** - Template engine (built-in Flask)

### Công cụ development
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
  - `name`
  - `unit` (kWh, m³, tháng...)
  - `price` (đơn giá)
  - `description`

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

## 9. Kế hoạch thực hiện

| Giai đoạn | Nội dung công việc | Dự kiến hoàn thành |
|-----------|-------------------|-------------------|
| **Tuần 1–2** | **Phân tích và thiết kế**<br>- Thiết kế database schema<br>- Vẽ sơ đồ ER<br>- Thiết kế giao diện mockup<br>- Setup project structure | Tuần 2 |
| **Tuần 3–4** | **Xây dựng chức năng cơ bản**<br>- Implement models và database<br>- Xây dựng authentication<br>- CRUD cho rooms và tenants<br>- Tạo giao diện cơ bản | Tuần 4 |
| **Tuần 5–6** | **Chức năng nâng cao**<br>- Quản lý hóa đơn và thanh toán<br>- Tạo hóa đơn hàng loạt<br>- Lịch sử thanh toán<br>- Phân quyền người dùng | Tuần 6 |
| **Tuần 7–8** | **Báo cáo và hoàn thiện**<br>- Xây dựng các trang báo cáo<br>- Hoàn thiện giao diện<br>- Testing và fix bugs<br>- Viết tài liệu hướng dẫn | Tuần 8 |
| **Tuần 9** | **Demo và báo cáo**<br>- Chuẩn bị demo<br>- Viết báo cáo cuối kỳ<br>- Deploy lên hosting (nếu có) | Tuần 9 |

---

## 10. Kết quả mong đợi

### Môi trường chạy
- **Localhost:** Chạy hoàn chỉnh trên máy local với SQLite
- **Hosting:** Có thể deploy lên PythonAnywhere, Heroku, hoặc VPS với PostgreSQL
- **URL demo:** http://127.0.0.1:5000 (local)

### Người dùng thử nghiệm
- Dự kiến: 5-10 người dùng thử (bạn bè, người thân, giảng viên)
- Feedback để cải thiện UX

### Demo mong muốn
Ứng dụng web hoàn chỉnh với:
- Đăng nhập được với 3 loại tài khoản
- Quản lý được ít nhất 10 phòng và 6 khách thuê
- Tạo được hóa đơn tự động
- Hiển thị báo cáo trực quan
- Giao diện đẹp, responsive

### Screenshots dự kiến
```
[Dashboard] - Tổng quan với số liệu thống kê
[Danh sách phòng] - Bảng danh sách với trạng thái
[Form thêm khách] - Form nhập liệu rõ ràng
[Chi tiết hóa đơn] - Hiển thị đầy đủ thông tin và lịch sử thanh toán
[Báo cáo doanh thu] - Biểu đồ hoặc bảng số liệu
```

---

## 11. Cam kết

Tôi, **Hồ Hữu Khải**, cam kết:

- Bài toán và sản phẩm là do cá nhân tự phát triển, không sao chép mã nguồn của người khác.
- Tất cả code được viết bởi bản thân hoặc có tham khảo từ tài liệu chính thống (Flask documentation, Bootstrap documentation).
- Tôi hiểu rõ toàn bộ codebase và có thể giải thích bất kỳ phần nào trong dự án.
- Tôi đồng ý rằng việc trùng đề tài hoặc không đạt yêu cầu kỹ thuật có thể ảnh hưởng đến điểm cuối kỳ.
- Tôi sẽ hoàn thành dự án đúng tiến độ và chất lượng đã cam kết.

**Ký tên:** Hồ Hữu Khải

**Ngày:** 07/11/2025

---

## Phụ lục: Cấu trúc thư mục dự án

```
RoomMaster/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms
│   ├── decorators.py         # Custom decorators (role required)
│   ├── errors.py             # Error handlers
│   ├── routes/               # Blueprints
│   │   ├── auth.py           # Đăng nhập/đăng xuất
│   │   ├── main.py           # Dashboard
│   │   ├── rooms.py          # Quản lý phòng
│   │   ├── tenants.py        # Quản lý khách thuê
│   │   ├── invoices.py       # Quản lý hóa đơn
│   │   ├── reports.py        # Báo cáo
│   │   └── users.py          # Quản lý người dùng
│   ├── services/             # Business logic layer
│   │   ├── room_service.py
│   │   ├── tenant_service.py
│   │   ├── invoice_service.py
│   │   ├── payment_service.py
│   │   └── report_service.py
│   ├── utils/                # Utilities
│   │   ├── helpers.py
│   │   └── logger.py
│   ├── templates/            # Jinja2 templates
│   └── static/               # CSS, JS, images
├── instance/                 # SQLite database
├── logs/                     # Log files
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── run.py                    # Entry point
└── seed_data.py              # Sample data
```
