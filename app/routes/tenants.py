from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Tenant, Room
from app.forms import TenantForm
from datetime import datetime
from app.decorators import manager_or_admin, admin_required

bp = Blueprint('tenants', __name__, url_prefix='/tenants')


# ============================================
# HELPER FUNCTION
# ============================================
def parse_date(date_string):
    """Convert dd/mm/yyyy string to date object"""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, '%d/%m/%Y').date()
    except ValueError:
        return None


# ============================================
# ROUTE 1: DANH SÁCH KHÁCH THUÊ
# ============================================
@bp.route('/')
@login_required
def list_tenants():
    """
    Hiển thị danh sách khách thuê
    Hỗ trợ tìm kiếm và lọc
    """
    
    # Lấy tham số tìm kiếm
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    # Query cơ bản
    query = Tenant.query
    
    # Tìm kiếm theo tên, CCCD, SĐT
    if search:
        query = query.filter(
            db.or_(
                Tenant.full_name.like(f'%{search}%'),
                Tenant.id_number.like(f'%{search}%'),
                Tenant.phone.like(f'%{search}%')
            )
        )
    
    # Lọc theo trạng thái
    if status_filter:
        query = query.filter(Tenant.status == status_filter)
    
    # Sắp xếp: Khách đang ở lên đầu
    tenants = query.order_by(
        Tenant.status.desc(),  # active trước inactive
        Tenant.full_name
    ).all()
    
    return render_template('tenants/list.html', 
                         tenants=tenants, 
                         search=search,
                         status_filter=status_filter)


# ============================================
# ROUTE 2: THÊM KHÁCH THUÊ
# ============================================
@bp.route('/add', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def add_tenant():
    """
    Thêm khách thuê mới
    """
    form = TenantForm()
    
    # Populate dropdown phòng (chỉ phòng trống)
    form.room_id.choices = [(0, '-- Chọn phòng --')] + [
        (room.id, f'{room.room_number} - {"{:,.0f}".format(room.price)} đ/tháng') 
        for room in Room.query.filter_by(status='available').order_by(Room.room_number).all()
    ]
    
    if form.validate_on_submit():
        # Kiểm tra phòng đã chọn
        if form.room_id.data == 0:
            flash('Vui lòng chọn phòng!', 'danger')
            return render_template('tenants/add.html', form=form)
        
        # Kiểm tra phòng còn trống không
        room = Room.query.get(form.room_id.data)
        if room.status != 'available':
            flash(f'Phòng {room.room_number} đã có người thuê!', 'danger')
            return render_template('tenants/add.html', form=form)
        
        # Tạo khách mới
        tenant = Tenant(
            full_name=form.full_name.data,
            id_number=form.id_number.data,
            phone=form.phone.data,
            email=form.email.data,
            date_of_birth=parse_date(form.date_of_birth.data),
            hometown=form.hometown.data,
            room_id=form.room_id.data,
            move_in_date=parse_date(form.move_in_date.data),
            move_out_date=parse_date(form.move_out_date.data),
            deposit=form.deposit.data or 0,
            is_main_tenant=form.is_main_tenant.data,
            status=form.status.data,
            notes=form.notes.data
        )
        
        # Cập nhật trạng thái phòng → Đã thuê
        room.status = 'occupied'
        
        # Lưu vào database
        db.session.add(tenant)
        db.session.commit()
        
        flash(f'Đã thêm khách thuê {tenant.full_name} vào phòng {room.room_number}!', 'success')
        return redirect(url_for('tenants.list_tenants'))
    
    return render_template('tenants/add.html', form=form)


# ============================================
# ROUTE 3: SỬA KHÁCH THUÊ
# ============================================
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def edit_tenant(id):
    """
    Chỉnh sửa thông tin khách thuê
    """
    tenant = Tenant.query.get_or_404(id)
    old_room_id = tenant.room_id  # Lưu phòng cũ
    
    # Truyền original_id_number và original_phone để bỏ qua validation
    form = TenantForm(original_id_number=tenant.id_number, original_phone=tenant.phone, obj=tenant)
    
    # Convert date objects to dd/mm/yyyy strings for form display
    if request.method == 'GET':
        if tenant.date_of_birth:
            form.date_of_birth.data = tenant.date_of_birth.strftime('%d/%m/%Y')
        if tenant.move_in_date:
            form.move_in_date.data = tenant.move_in_date.strftime('%d/%m/%Y')
        if tenant.move_out_date:
            form.move_out_date.data = tenant.move_out_date.strftime('%d/%m/%Y')
    
    # Populate dropdown phòng
    # Bao gồm: Phòng hiện tại + Phòng trống
    available_rooms = Room.query.filter(
        db.or_(
            Room.id == tenant.room_id,
            Room.status == 'available'
        )
    ).order_by(Room.room_number).all()
    
    form.room_id.choices = [
        (room.id, f'{room.room_number} - {"{:,.0f}".format(room.price)} đ/tháng') 
        for room in available_rooms
    ]
    
    if form.validate_on_submit():
        # Cập nhật thông tin
        tenant.full_name = form.full_name.data
        tenant.id_number = form.id_number.data
        tenant.phone = form.phone.data
        tenant.email = form.email.data
        tenant.date_of_birth = parse_date(form.date_of_birth.data)
        tenant.hometown = form.hometown.data
        tenant.move_in_date = parse_date(form.move_in_date.data)
        tenant.move_out_date = parse_date(form.move_out_date.data)
        tenant.deposit = form.deposit.data or 0
        tenant.is_main_tenant = form.is_main_tenant.data
        tenant.status = form.status.data
        tenant.notes = form.notes.data
        
        # Nếu đổi phòng
        if form.room_id.data != old_room_id:
            # Phòng cũ → Trống
            old_room = Room.query.get(old_room_id)
            if old_room:
                old_room.status = 'available'
            
            # Phòng mới → Đã thuê
            new_room = Room.query.get(form.room_id.data)
            new_room.status = 'occupied'
            tenant.room_id = form.room_id.data
            
            flash(f'Đã chuyển {tenant.full_name} từ phòng {old_room.room_number} sang {new_room.room_number}!', 'info')
        
        db.session.commit()
        
        flash(f'Đã cập nhật thông tin khách {tenant.full_name}!', 'success')
        return redirect(url_for('tenants.list_tenants'))
    
    return render_template('tenants/edit.html', form=form, tenant=tenant)


# ============================================
# ROUTE 4: ĐÁNH DẤU CHUYỂN ĐI
# ============================================
@bp.route('/checkout/<int:id>')
@login_required
@manager_or_admin
def checkout_tenant(id):
    """
    Đánh dấu khách đã chuyển đi
    Giải phóng phòng
    """
    from app.models import Invoice
    tenant = Tenant.query.get_or_404(id)
    
    # Kiểm tra hóa đơn chưa thanh toán qua room
    unpaid_invoices = Invoice.query.filter(
        Invoice.room_id == tenant.room_id,
        Invoice.status.in_(['unpaid', 'partial'])
    ).count()
    
    if unpaid_invoices > 0:
        flash(f'{tenant.full_name} còn {unpaid_invoices} hóa đơn chưa thanh toán. Vui lòng thanh toán trước!', 'warning')
        return redirect(url_for('tenants.list_tenants'))
    
    # Đổi trạng thái khách → moved_out
    tenant.status = 'moved_out'
    tenant.move_out_date = datetime.now().date()
    
    # Giải phóng phòng → Trống
    if tenant.room:
        tenant.room.status = 'available'
    
    db.session.commit()
    
    flash(f'{tenant.full_name} đã chuyển đi. Phòng {tenant.room.room_number} đã được giải phóng.', 'success')
    return redirect(url_for('tenants.list_tenants'))


# ============================================
# ROUTE 5: XÓA KHÁCH THUÊ
# ============================================
@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete_tenant(id):
    """
    Xóa khách thuê khỏi hệ thống
    """
    from app.models import Invoice
    tenant = Tenant.query.get_or_404(id)
    
    # Kiểm tra có hóa đơn không (qua room)
    invoice_count = Invoice.query.filter_by(room_id=tenant.room_id).count()
    if invoice_count > 0:
        flash(f'Không thể xóa {tenant.full_name} vì phòng đã có hóa đơn!', 'danger')
        return redirect(url_for('tenants.list_tenants'))
    
    # Giải phóng phòng nếu đang thuê
    if tenant.status == 'active' and tenant.room:
        tenant.room.status = 'available'
    
    # Xóa khách
    tenant_name = tenant.full_name
    db.session.delete(tenant)
    db.session.commit()
    
    flash(f'Đã xóa khách {tenant_name}!', 'success')
    return redirect(url_for('tenants.list_tenants'))


# ============================================
# ROUTE 6: CHI TIẾT KHÁCH THUÊ
# ============================================
@bp.route('/detail/<int:id>')
@login_required
def detail_tenant(id):
    """
    Xem chi tiết khách thuê
    """
    from app.models import Invoice
    tenant = Tenant.query.get_or_404(id)
    
    # Lấy hóa đơn gần nhất qua room
    recent_invoices = Invoice.query.filter_by(room_id=tenant.room_id).order_by(
        Invoice.created_at.desc()
    ).limit(10).all()
    
    # Tính tổng công nợ (hóa đơn chưa thanh toán)
    unpaid_invoices = Invoice.query.filter(
        Invoice.room_id == tenant.room_id,
        Invoice.status.in_(['unpaid', 'partial'])
    ).all()
    
    total_debt = sum(invoice.total_amount for invoice in unpaid_invoices)
    
    return render_template('tenants/detail.html', 
                         tenant=tenant,
                         recent_invoices=recent_invoices,
                         total_debt=total_debt)
