"""
============================================
SERVICES ROUTES - Quản lý dịch vụ (Chỉ Admin)
============================================
Quản lý các dịch vụ: Điện, Nước, Internet, Rác, Bảo vệ, v.v.
Chỉ admin mới có quyền thêm/sửa/xóa dịch vụ

Routes:
    - list_services: Danh sách dịch vụ
    - create_service: Tạo dịch vụ mới
    - edit_service: Chỉnh sửa dịch vụ
    - delete_service: Xóa dịch vụ
    - toggle_status: Bật/tắt dịch vụ
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service
from app.decorators import admin_required

bp = Blueprint('services', __name__, url_prefix='/services')


# ============================================
# 1. DANH SÁCH DỊCH VỤ
# ============================================
@bp.route('/')
@login_required
@admin_required
def list_services():
    """
    Hiển thị danh sách tất cả dịch vụ
    Chỉ admin mới truy cập được
    """
    services = Service.query.order_by(Service.name).all()
    return render_template('services/list.html', services=services)


# ============================================
# 2. TẠO DỊCH VỤ MỚI
# ============================================
@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_service():
    """
    Tạo dịch vụ mới
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        unit = request.form.get('unit', '').strip()
        price = request.form.get('price', 0, type=float)
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        # Validation
        if not name:
            flash('❌ Tên dịch vụ không được để trống!', 'danger')
            return redirect(url_for('services.create_service'))
        
        if price < 0:
            flash('❌ Đơn giá không được âm!', 'danger')
            return redirect(url_for('services.create_service'))
        
        # Kiểm tra trùng tên
        existing = Service.query.filter_by(name=name).first()
        if existing:
            flash(f'⚠️ Dịch vụ "{name}" đã tồn tại!', 'warning')
            return redirect(url_for('services.create_service'))
        
        # Tạo dịch vụ mới
        service = Service(
            name=name,
            unit=unit,
            price=price,
            description=description,
            is_active=is_active
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash(f'✅ Đã tạo dịch vụ "{name}" thành công!', 'success')
        return redirect(url_for('services.list_services'))
    
    # GET: Hiển thị form
    return render_template('services/create.html')


# ============================================
# 3. CHỈNH SỬA DỊCH VỤ
# ============================================
@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    """
    Chỉnh sửa thông tin dịch vụ
    """
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        unit = request.form.get('unit', '').strip()
        price = request.form.get('price', 0, type=float)
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        # Validation
        if not name:
            flash('❌ Tên dịch vụ không được để trống!', 'danger')
            return redirect(url_for('services.edit_service', id=id))
        
        if price < 0:
            flash('❌ Đơn giá không được âm!', 'danger')
            return redirect(url_for('services.edit_service', id=id))
        
        # Kiểm tra trùng tên (trừ chính nó)
        existing = Service.query.filter(
            Service.name == name,
            Service.id != id
        ).first()
        if existing:
            flash(f'⚠️ Dịch vụ "{name}" đã tồn tại!', 'warning')
            return redirect(url_for('services.edit_service', id=id))
        
        # Cập nhật
        service.name = name
        service.unit = unit
        service.price = price
        service.description = description
        service.is_active = is_active
        
        db.session.commit()
        
        flash(f'✅ Đã cập nhật dịch vụ "{name}" thành công!', 'success')
        return redirect(url_for('services.list_services'))
    
    # GET: Hiển thị form
    return render_template('services/edit.html', service=service)


# ============================================
# 4. XÓA DỊCH VỤ
# ============================================
@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_service(id):
    """
    Xóa dịch vụ
    Cảnh báo: Nên kiểm tra xem dịch vụ có đang được sử dụng không
    """
    service = Service.query.get_or_404(id)
    service_name = service.name
    
    try:
        db.session.delete(service)
        db.session.commit()
        flash(f'✅ Đã xóa dịch vụ "{service_name}" thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Không thể xóa dịch vụ "{service_name}". Có thể đang được sử dụng trong hóa đơn.', 'danger')
    
    return redirect(url_for('services.list_services'))


# ============================================
# 5. BẬT/TẮT DỊCH VỤ
# ============================================
@bp.route('/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_status(id):
    """
    Bật/tắt trạng thái hoạt động của dịch vụ
    Thay vì xóa, có thể tắt dịch vụ không dùng nữa
    """
    service = Service.query.get_or_404(id)
    service.is_active = not service.is_active
    
    db.session.commit()
    
    status = 'kích hoạt' if service.is_active else 'tắt'
    flash(f'✅ Đã {status} dịch vụ "{service.name}"!', 'success')
    
    return redirect(url_for('services.list_services'))
