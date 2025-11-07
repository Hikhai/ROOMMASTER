# Báo cáo dự án — RoomMaster

- Họ tên: Ho Hữu Khải
- Mã SV: 21T1020436
- Ngày: 07/11/2025

## 1. Mục tiêu dự án
RoomMaster là một ứng dụng quản lý thuê phòng (room/rental management) được xây dựng bằng Flask nhằm quản lý phòng, khách thuê, hóa đơn, và thanh toán. Mục tiêu của dự án là tạo một hệ thống nhỏ gọn, dễ mở rộng và dễ bảo trì, áp dụng kiến trúc có lớp (Service Layer) và các best-practice cho dự án Flask.

## 2. Tính năng chính
- Quản lý người dùng với vai trò (admin, manager, viewer) và phân quyền UI.
- CRUD cho phòng, khách thuê, dịch vụ, hóa đơn và thanh toán.
- Tạo hóa đơn đơn lẻ và tạo hàng loạt (bulk invoices) với kiểm tra trùng lặp (unique constraint trên room_id, month, year).
- Lịch sử thanh toán cho mỗi hóa đơn và hỗ trợ thanh toán một phần.
- Báo cáo doanh thu, công nợ và tỷ lệ lấp đầy.
- Giao diện UI cơ bản dùng Bootstrap; hàng có thể click để đi tới trang chi tiết tương ứng.
- Seed data để khởi tạo dữ liệu mẫu (admin, manager, viewer, nhiều phòng và khách thuê).

## 3. Kiến trúc và quyết định kỹ thuật
- Framework: Flask (App Factory pattern) với Blueprints cho từng module (auth, rooms, tenants, invoices, reports, users).
- ORM: SQLAlchemy.
- Thiết kế: Service Layer (các file `app/services/*`) để tách business logic khỏi routes/templates.
- Helpers: `app/utils/helpers.py` và `app/utils/logger.py` để chuẩn hóa định dạng, logging và tiện ích chung.
- Error handling: Tập trung trong `app/errors.py` và templates lỗi `app/templates/errors/`.
- Templates: Jinja2, Bootstrap 5; macros chung nằm ở `_macros.html`.
- Logging: RotatingFileHandler, log vào `logs/roommaster.log`.

## 4. Cấu trúc chính của repository
Các mục chính (đã chỉnh sửa/ thêm):
- `app/` - package chính chứa blueprints, services, utils, templates, static.
- `app/services/` - `room_service.py`, `tenant_service.py`, `invoice_service.py`, `payment_service.py`, `report_service.py`.
- `app/utils/` - `helpers.py`, `logger.py`.
- `app/errors.py` - centralized error handlers.
- `seed_data.py` - script tạo dữ liệu mẫu.
- `requirements.txt` - list phụ thuộc.
- Tài liệu: `README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `GITHUB_SETUP.md`, `CLEANUP_SUMMARY.md`.

## 5. Các vấn đề đã gặp & cách giải quyết
- Lỗi TemplateSyntaxError trong `create_bulk.html`: Sửa cấu trúc Jinja2, loại bỏ nested/malformed tags.
- Sắp xếp lịch sử thanh toán: Sử dụng filter `|sort(attribute='payment_date', reverse=True)` trong Jinja để đảm bảo thứ tự mong muốn.
- Kiểm tra trùng lặp hóa đơn: Thêm unique constraint ở model `Invoice` trên `(room_id, month, year)` và xử lý trong service/migration.
- Thiết kế lại code: Tách business logic ra `app/services/` để dễ bảo trì và test.

## 6. Hướng dẫn chạy dự án (phát triển)
1. Tạo virtual environment và cài dependencies:

```powershell
# Windows PowerShell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Khởi tạo database (ví dụ SQLite) và seed dữ liệu:

```powershell
# nếu dùng Flask-Migrate: flask db upgrade
python seed_data.py
```

3. Chạy ứng dụng:

```powershell
python run.py
# hoặc
flask run
```

4. Mở trình duyệt tại `http://127.0.0.1:5000`.

## 7. Dữ liệu mẫu
Script `seed_data.py` đã tạo các bản ghi mẫu gồm:
- 3 users: admin, manager, viewer
- 5 services
- 10 rooms (trong đó 6 room có khách)
- 6 tenants

## 8. Kiểm thử nhanh
- Đã chạy: kiểm tra khởi tạo app (`from app import create_app; app = create_app()`) thành công.
- Đã kiểm tra các template chính (danh sách phòng, tạo hóa đơn, tạo hàng loạt, trang thanh toán) sau khi sửa lỗi template.

## 9. Những việc còn làm / Nâng cấp gợi ý
- Đẩy repo lên GitHub và cấu hình CI (GitHub Actions) để chạy tests và lint.
- Viết test tự động: unit tests cho `app/services/*` và integration tests cho routes quan trọng.
- Dockerize ứng dụng cho deploy/staging.
- Chuyển DB sang PostgreSQL cho môi trường production; viết hướng dẫn migration và cấu hình environment.
- Thêm role-based access control chi tiết và audit logs.

## 10. Ghi chú đóng góp
- Tác giả mã nguồn và các thay đổi cấu trúc: nhiều file đã được thêm/sửa để chuyển sang Service Layer và thêm logging/error handling. Tất cả thay đổi đã được commit vào repository local.

---

Tôi đã tạo file báo cáo này trong repository. Nếu cần, tôi có thể:
- Thêm nội dung chi tiết hơn từng phần (mô tả model, ERD, đoạn mã mẫu).
- Export sang PDF/DOCX.
- Commit và push ngay lập tức lên GitHub nếu bạn cho remote repo URL hoặc muốn tôi thiết lập remote.
