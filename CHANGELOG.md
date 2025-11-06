# Changelog

All notable changes to RoomMaster project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-06

### 🎉 Major Restructure

#### Added
- **Service Layer Pattern**: Tách business logic vào `app/services/`
  - `RoomService`: Logic quản lý phòng
  - `TenantService`: Logic quản lý khách thuê
  - `InvoiceService`: Logic quản lý hóa đơn
  - `PaymentService`: Logic quản lý thanh toán
  - `ReportService`: Logic báo cáo thống kê

- **Utils Package**: Helper functions và utilities
  - `helpers.py`: Format, parse, decorators, validators
  - `logger.py`: Logging configuration với rotation

- **Error Handling System**:
  - Centralized error handlers trong `app/errors.py`
  - Custom error pages (400, 403, 404, 500)
  - Automatic database rollback on errors
  - Structured logging

- **Template Filters**: Jinja2 custom filters
  - `currency`: Format tiền tệ
  - `date`: Format ngày tháng
  - `status_badge`: Bootstrap badge class

- **Documentation**:
  - `.env.example`: Environment variables template
  - `ARCHITECTURE.md`: Detailed architecture documentation
  - Enhanced `README.md` với full setup guide

#### Changed
- **App Factory**: Enhanced với error handlers và logging
- **Project Structure**: Reorganized theo layered architecture
- **Logging**: Production-ready với rotating file handler

#### Technical Improvements
- Better separation of concerns (SoC)
- Improved code reusability
- Enhanced maintainability
- Production-ready logging
- Better error handling

---

## [1.5.0] - 2025-11-05

### Added
- **Active Navbar**: Tự động highlight menu item hiện tại
- **Clickable Table Rows**: Click vào hàng để xem chi tiết
- **Permission-based UI**: Ẩn/hiện buttons theo role

### Fixed
- Form validation: Password field có thể để trống khi edit user
- Template syntax errors trong create_bulk.html
- Payment sorting với dynamic relationships
- Endpoint names consistency

---

## [1.0.0] - 2025-11-04

### Added
- **Core Features**:
  - User authentication & authorization (3 roles)
  - Room management (CRUD)
  - Tenant management (CRUD)
  - Invoice management với bulk creation
  - Payment tracking (partial payments supported)
  - Reports & statistics

- **Database**:
  - SQLite với SQLAlchemy ORM
  - Unique constraint: (room_id, month, year) trên Invoice
  - Proper relationships và foreign keys

- **UI/UX**:
  - Bootstrap 5 responsive design
  - Toast notifications
  - Loading states
  - Form validations
  - Smooth transitions

- **Security**:
  - Password hashing
  - CSRF protection
  - Role-based access control
  - Session management

### Database Schema
- User model với role-based permissions
- Room model với status tracking
- Tenant model với move-in/out dates
- Service model for utilities
- Invoice model với unique constraint
- Payment model với multiple payments support

---

## [Unreleased]

### Planned Features
- [ ] REST API endpoints
- [ ] Email notifications
- [ ] PDF export cho invoices
- [ ] Excel export cho reports
- [ ] Automated database backups
- [ ] Multi-tenancy support
- [ ] Mobile responsive improvements
- [ ] Advanced search & filters
- [ ] Chart visualizations
- [ ] File uploads (contracts, photos)

### Technical Debt
- [ ] Unit tests
- [ ] Integration tests
- [ ] API documentation
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## Version History Summary

- **v2.0.0**: Major restructure với Service Layer Pattern
- **v1.5.0**: UI improvements & bug fixes
- **v1.0.0**: Initial release với core features

---

## Migration Guide

### From v1.x to v2.0

**No database changes required** - cấu trúc database giữ nguyên.

**Code changes**:
- Routes có thể sử dụng services để tách logic (optional)
- New utility functions available trong `app/utils/helpers.py`
- Error pages tự động handle bởi `app/errors.py`

**Recommended actions**:
1. Copy `.env.example` thành `.env` nếu chưa có
2. Update `SECRET_KEY` trong `.env`
3. Kiểm tra logs folder permissions
4. Review ARCHITECTURE.md để hiểu cấu trúc mới

### Breaking Changes
None - backward compatible với v1.x

---

## Contributors

- RoomMaster Development Team

## Links

- [GitHub Repository](https://github.com/yourusername/roommaster)
- [Documentation](./README.md)
- [Architecture](./ARCHITECTURE.md)
