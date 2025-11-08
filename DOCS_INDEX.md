# 📌 ROOMMASTER - TÀI LIỆU HƯỚNG DẪN

## 📂 CÁC FILE TÀI LIỆU

### 1. **README.md** (15KB)
**Nội dung:** Giới thiệu dự án, cài đặt, và tính năng tổng quan
- Giới thiệu RoomMaster
- Tính năng nổi bật (Authentication, CRUD, Reports, Dark Mode...)
- Kiến trúc dự án (MVC + Service Layer)
- Cài đặt và chạy ứng dụng
- Requirements (Python 3.10+, Flask 3.0.0, SQLAlchemy...)
- Thông tin database models
- Deployment options

**Đọc khi:** Bắt đầu với dự án, cần cài đặt và chạy

---

### 2. **HoHuuKhai_21T1020436.md** (26KB) ⭐
**Nội dung:** Báo cáo đề tài môn Phần mềm mã nguồn mở
- Bối cảnh và vấn đề thực tế
- Mục tiêu và phạm vi ứng dụng
- Phân tích người dùng (Admin, Manager, Viewer)
- Các chức năng chính (CRUD, Invoice, Payment, Reports...)
- Giao diện UI/UX (Dark Mode, Responsive, Modern Footer)
- Công nghệ sử dụng (Flask 3.0.0, SQLAlchemy 3.1.1, Bootstrap 5.3.0...)
- Cấu trúc dữ liệu (7 models: User, Room, Tenant, Invoice, Payment, Service...)
- **Kết quả đã hoàn thành 100%**
- Cam kết và cấu trúc thư mục chi tiết

**Đọc khi:** Cần hiểu toàn bộ dự án, nộp báo cáo, demo cho giảng viên

---

### 3. **GUIDE.md** (5KB)
**Nội dung:** Hướng dẫn sử dụng từng chức năng
- Khởi động ứng dụng (python run.py)
- Quản lý database (init-db, seed-db)
- Tài khoản demo (admin/manager/viewer)
- Hướng dẫn chi tiết từng chức năng:
  * Quản lý phòng
  * Quản lý khách thuê
  * Tạo hóa đơn (đơn lẻ và hàng loạt)
  * Thanh toán
  * Báo cáo
  * Quản lý dịch vụ (Admin)
  * Quản lý người dùng (Admin)
- Commands hữu ích

**Đọc khi:** Muốn biết cách sử dụng từng tính năng cụ thể

---

### 4. **WORKFLOW.md** (27KB) 🔥
**Nội dung:** Luồng hoạt động chi tiết của code
- Kiến trúc tổng quan (MVC + Service Layer)
- Luồng xác thực (Login, Authorization)
- Luồng quản lý phòng (CRUD với code examples)
- Luồng quản lý khách thuê (Check-in/Check-out flow)
- Luồng quản lý hóa đơn (Create single, Bulk create)
- Luồng thanh toán (Record payment, Partial payment)
- Luồng báo cáo (Revenue, Occupancy reports)
- Luồng quản lý dịch vụ (CRUD, Toggle status)
- Luồng giao diện (Dark Mode toggle, UI flow)
- Error Handling Flow
- Logging Flow
- Transaction Management

**Đọc khi:** Cần hiểu sâu cách code hoạt động, maintain/extend project

---

### 5. **DEPLOYMENT.md** (NEW! 🚀)
**Nội dung:** Hướng dẫn triển khai production
- Chuẩn bị trước khi deploy
- Tối ưu hóa (database, static files)
- Deploy lên VPS/Server (Nginx + Gunicorn)
- Deploy lên PythonAnywhere
- Deploy lên Heroku
- Bảo mật checklist
- Monitoring & Maintenance
- Backup strategies

**Đọc khi:** Cần deploy lên production server thực tế

---

### 6. **DEPLOY_FREE.md** (NEW! 🆓)
**Nội dung:** Hướng dẫn deploy miễn phí
- So sánh các nền tảng miễn phí
- **PythonAnywhere** (Khuyến nghị ⭐⭐⭐⭐⭐)
  * Setup chi tiết từng bước
  * WSGI configuration
  * Troubleshooting
- **Render.com** (PostgreSQL miễn phí)
- **Railway.app** (500h/tháng)
- **Fly.io** (Persistent storage)
- Khuyến nghị theo mục đích
- Quick start 5 phút

**Đọc khi:** Muốn deploy miễn phí cho demo/học tập

---

### 7. **PRODUCTION_CHECKLIST.md** (NEW! ✅)
**Nội dung:** Checklist xuất sản phẩm
- Chuẩn bị project
- Tối ưu hóa
- Bảo mật
- Testing checklist
- Deliverables
- Hướng dẫn cho người dùng cuối
- Support checklist
- Final check

**Đọc khi:** Sẵn sàng giao sản phẩm cho người dùng cuối

---

### 7. **DOCS_INDEX.md** (5KB) 📌
**Nội dung:** File này - Chỉ mục tài liệu và lộ trình đọc
- Tóm tắt nội dung từng file tài liệu
- Lộ trình đọc tài liệu theo từng đối tượng
- Thống kê dự án
- Quick start guide

**Đọc khi:** Mới bắt đầu, không biết đọc file nào trước

---

## 🎯 LỘ TRÌNH ĐỌC TÀI LIỆU

### Cho người dùng cuối:
```
1. PRODUCTION_CHECKLIST.md → Checklist cài đặt
2. README.md               → Hiểu dự án và tính năng
3. Chạy: python run.py     → Trải nghiệm ứng dụng
4. GUIDE.md                → Học cách sử dụng chi tiết
```

### Cho người deploy production:
```
1. README.md               → Tổng quan dự án
2. DEPLOYMENT.md           → Hướng dẫn deploy chi tiết
3. PRODUCTION_CHECKLIST.md → Checklist trước deploy
4. optimize_production.py  → Chạy optimization
```

### Cho người mới bắt đầu:
```
1. DOCS_INDEX.md (file này) → Tổng quan tài liệu
2. README.md               → Hiểu dự án và cài đặt
3. Chạy: python run.py     → Trải nghiệm ứng dụng
4. GUIDE.md                → Học cách sử dụng
```

### Cho người muốn hiểu sâu code:
```
1. README.md               → Xem kiến trúc
2. WORKFLOW.md             → Hiểu luồng hoạt động chi tiết
3. Source code             → Đọc code trong app/
4. HoHuuKhai_21T1020436.md → Báo cáo đầy đủ
```

### Cho giảng viên/người đánh giá:
```
1. HoHuuKhai_21T1020436.md → Báo cáo đề tài đầy đủ
2. README.md               → Tính năng và kiến trúc
3. WORKFLOW.md             → Kiến trúc kỹ thuật chi tiết
4. Demo live               → http://127.0.0.1:5000
```

---

## 📊 THỐNG KÊ DỰ ÁN

### Tài liệu
- 📄 Tổng: 7 files markdown
- 📏 Tổng dung lượng: ~95KB
- 📝 Tổng số dòng: ~2500+ dòng documentation

### Code
- 🐍 Python files: 28+ files (bao gồm optimization scripts)
- 🎨 HTML templates: 30+ files
- 📦 Lines of Code: ~3000+ Python, ~1000+ CSS, ~200+ JS
- 🗄️ Database models: 7 models
- 🔌 API endpoints: 50+ routes

### Tính năng
- ✅ Authentication & Authorization: 100%
- ✅ CRUD Operations: 100%
- ✅ Business Logic: 100%
- ✅ Reports & Analytics: 100%
- ✅ UI/UX (Dark Mode, Responsive): 100%
- ✅ Documentation: 100%
- ✅ Production Optimization: 100%
- ✅ Security Enhancements: 100%

### Tối ưu Production (NEW!)
- ⚡ Database indexes optimization
- ⚡ Query performance optimization
- ⚡ CSS/JS minification
- ⚡ Security headers
- ⚡ CSRF protection
- ⚡ Rate limiting
- ⚡ Session security
- ⚡ Error handling

---

## 🚀 QUICK START

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Khởi tạo database
python seed_data.py

# 3. Tối ưu production (tùy chọn)
python optimize_production.py

# 4. Minify static files (tùy chọn)
python minify_static.py

# 5. Chạy ứng dụng
python run.py

# 6. Truy cập
http://127.0.0.1:5000

# 7. Đăng nhập
Username: admin
Password: admin123
```

---

## �️ SCRIPTS HỖ TRỢ

### 1. **optimize_production.py** (NEW!)
Tối ưu database cho production:
- Thêm indexes cho queries nhanh hơn
- Optimize SQLite settings (WAL mode, cache)
- Analyze database statistics
- Display database statistics

```bash
python optimize_production.py
```

### 2. **minify_static.py** (NEW!)
Minify CSS và JavaScript:
- Giảm 30-40% kích thước CSS
- Giảm 20-30% kích thước JavaScript
- Tạo files .min.css và .min.js

```bash
python minify_static.py
```

### 3. **seed_data.py**
Tạo dữ liệu mẫu:
- 3 users (admin, manager, viewer)
- 10 rooms
- 6 tenants
- 5 services
- Sample invoices

```bash
python seed_data.py
```

---

## �📞 HỖ TRỢ

- **Sinh viên:** Hồ Hữu Khải
- **MSSV:** 21T1020436
- **Đề tài:** Hệ thống quản lý phòng trọ RoomMaster bằng Flask
- **Ngày hoàn thành:** 08/11/2025
- **Version:** 1.0.0 (Production Ready)

---

**Chúc bạn sử dụng RoomMaster hiệu quả! 🎉**
