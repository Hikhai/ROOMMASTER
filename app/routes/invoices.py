"""
============================================
INVOICES ROUTES - Quản lý hóa đơn
============================================
Cấu trúc đơn giản với trường trực tiếp cho điện/nước
Không dùng InvoiceItem relationship

Routes:
    - list_invoices: Danh sách hóa đơn với filter
    - create_invoice: Tạo hóa đơn đơn lẻ
    - view_invoice: Xem chi tiết hóa đơn
    - edit_invoice: Chỉnh sửa hóa đơn
    - payment_invoice: Ghi nhận thanh toán
    - delete_invoice: Xóa hóa đơn
    - create_bulk_invoices: Tạo hóa đơn hàng loạt
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Invoice, Room, Payment, Service
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.decorators import manager_or_admin, admin_required

bp = Blueprint('invoices', __name__, url_prefix='/invoices')


# ============================================
# HELPER FUNCTIONS
# ============================================
def validate_invoice_readings(electric_old, electric_new, water_old, water_new):
    """
    Validate meter readings
    
    Args:
        electric_old: Old electricity reading
        electric_new: New electricity reading
        water_old: Old water reading
        water_new: New water reading
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if electric_new < electric_old:
        return False, '⚠️ Số điện mới phải >= số điện cũ!'
    
    if water_new < water_old:
        return False, '⚠️ Số nước mới phải >= số nước cũ!'
    
    return True, None


# ============================================
# 1. DANH SÁCH HÓA ĐƠN
# ============================================
@bp.route('/')
@login_required
def list_invoices():
    """
    Hiển thị danh sách hóa đơn với tìm kiếm & lọc
    """
    # Lấy tham số từ URL
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    room_number = request.args.get('room_number', '').strip()
    
    # Query cơ bản
    query = Invoice.query.join(Room)
    
    # Lọc theo trạng thái
    if status:
        query = query.filter(Invoice.status == status)
    
    # Lọc theo tháng/năm
    if month and year:
        query = query.filter(and_(Invoice.month == month, Invoice.year == year))
    elif year:
        query = query.filter(Invoice.year == year)
    
    # Tìm kiếm theo số phòng
    if room_number:
        query = query.filter(Room.room_number.contains(room_number))
    
    # Sắp xếp: Mới nhất trước
    invoices = query.order_by(Invoice.year.desc(), Invoice.month.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    return render_template('invoices/list.html', 
                         invoices=invoices,
                         status=status,
                         month=month,
                         year=year,
                         room_number=room_number)


# ============================================
# 2. TẠO HÓA ĐƠN MỚI (ĐƠN LẺ)
# ============================================
@bp.route('/create', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def create_invoice():
    """
    Tạo hóa đơn cho 1 phòng
    Tự động lấy giá phòng, cho phép nhập chỉ số điện/nước
    """
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        room_id = request.form.get('room_id', type=int)
        month = request.form.get('month', type=int)
        year = request.form.get('year', type=int)
        
        # Chỉ số điện
        electric_old = request.form.get('electric_old', 0, type=float)
        electric_new = request.form.get('electric_new', 0, type=float)
        electric_unit_price = request.form.get('electric_unit_price', 3500, type=float)
        
        # Chỉ số nước
        water_old = request.form.get('water_old', 0, type=float)
        water_new = request.form.get('water_new', 0, type=float)
        water_unit_price = request.form.get('water_unit_price', 20000, type=float)
        
        # Phí khác
        other_fees = request.form.get('other_fees', 0, type=float)
        
        notes = request.form.get('notes', '').strip()
        
        # Validation
        room = Room.query.get_or_404(room_id)
        
        # Kiểm tra trùng hóa đơn
        existing = Invoice.query.filter_by(room_id=room_id, month=month, year=year).first()
        if existing:
            flash(f'⚠️ Phòng {room.room_number} đã có hóa đơn tháng {month}/{year}!', 'warning')
            return redirect(url_for('invoices.create_invoice'))
        
        # Kiểm tra chỉ số
        is_valid, error_msg = validate_invoice_readings(electric_old, electric_new, water_old, water_new)
        if not is_valid:
            flash(error_msg, 'danger')
            return redirect(url_for('invoices.create_invoice'))
        
        # Tạo hóa đơn mới
        invoice = Invoice(
            room_id=room_id,
            month=month,
            year=year,
            room_price=room.price,  # Tự động lấy từ Room
            electric_old=electric_old,
            electric_new=electric_new,
            electric_unit_price=electric_unit_price,
            water_old=water_old,
            water_new=water_new,
            water_unit_price=water_unit_price,
            other_fees=other_fees,
            notes=notes,
            created_by=current_user.id,
            due_date=datetime.now() + timedelta(days=7)  # Hạn thanh toán: 7 ngày
        )
        
        # Tính tổng tiền
        invoice.calculate_total()
        
        db.session.add(invoice)
        db.session.commit()
        
        flash(f'✅ Đã tạo hóa đơn phòng {room.room_number} tháng {month}/{year}!', 'success')
        return redirect(url_for('invoices.view_invoice', id=invoice.id))
    
    # GET: Hiển thị form
    # Chỉ lấy phòng đang cho thuê
    rooms = Room.query.filter_by(status='occupied').order_by(Room.room_number).all()
    
    # Lấy dịch vụ để hiển thị đơn giá tham khảo
    services = Service.query.filter_by(is_active=True).all()
    
    # Lấy tháng hiện tại
    now = datetime.now()
    
    return render_template('invoices/create.html',
                         rooms=rooms,
                         services=services,
                         current_month=now.month,
                         current_year=now.year)


# ============================================
# 3. XEM CHI TIẾT HÓA ĐƠN
# ============================================
@bp.route('/<int:id>')
@login_required
def view_invoice(id):
    """
    Hiển thị chi tiết hóa đơn
    Bao gồm: thông tin phòng, chi tiết tính toán, lịch sử thanh toán
    """
    invoice = Invoice.query.get_or_404(id)
    
    # Lấy danh sách thanh toán
    payments = invoice.payments.order_by(Payment.payment_date.desc()).all()
    
    # Tính toán
    electric_usage = invoice.electric_new - invoice.electric_old
    water_usage = invoice.water_new - invoice.water_old
    
    return render_template('invoices/view.html',
                         invoice=invoice,
                         payments=payments,
                         electric_usage=electric_usage,
                         water_usage=water_usage)


# ============================================
# 4. CHỈNH SỬA HÓA ĐƠN
# ============================================
@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def edit_invoice(id):
    """
    Chỉnh sửa hóa đơn (chỉ cho phép nếu chưa thanh toán đủ)
    """
    invoice = Invoice.query.get_or_404(id)
    
    # Không cho sửa hóa đơn đã thanh toán đầy đủ
    if invoice.status == 'paid':
        flash('⚠️ Không thể sửa hóa đơn đã thanh toán đủ!', 'warning')
        return redirect(url_for('invoices.view_invoice', id=invoice.id))
    
    if request.method == 'POST':
        # Cập nhật thông tin
        invoice.electric_old = request.form.get('electric_old', 0, type=float)
        invoice.electric_new = request.form.get('electric_new', 0, type=float)
        invoice.electric_unit_price = request.form.get('electric_unit_price', 3500, type=float)
        
        invoice.water_old = request.form.get('water_old', 0, type=float)
        invoice.water_new = request.form.get('water_new', 0, type=float)
        invoice.water_unit_price = request.form.get('water_unit_price', 20000, type=float)
        
        invoice.other_fees = request.form.get('other_fees', 0, type=float)
        invoice.notes = request.form.get('notes', '').strip()
        
        # Validation
        is_valid, error_msg = validate_invoice_readings(
            invoice.electric_old, invoice.electric_new,
            invoice.water_old, invoice.water_new
        )
        if not is_valid:
            flash(error_msg, 'danger')
            return redirect(url_for('invoices.edit_invoice', id=invoice.id))
        
        # Tính lại tổng tiền
        invoice.calculate_total()
        
        # Cập nhật trạng thái
        invoice.update_status()
        
        db.session.commit()
        
        flash('✅ Đã cập nhật hóa đơn!', 'success')
        return redirect(url_for('invoices.view_invoice', id=invoice.id))
    
    # GET: Hiển thị form
    return render_template('invoices/edit.html', invoice=invoice)


# ============================================
# 5. THANH TOÁN HÓA ĐƠN
# ============================================
@bp.route('/<int:id>/payment', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def payment_invoice(id):
    """
    Ghi nhận thanh toán cho hóa đơn
    Hỗ trợ thanh toán từng phần (partial payment)
    """
    invoice = Invoice.query.get_or_404(id)
    
    if request.method == 'POST':
        amount = request.form.get('amount', 0, type=float)
        payment_method = request.form.get('payment_method', 'cash')
        payment_date_str = request.form.get('payment_date')
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if amount <= 0:
            flash('⚠️ Số tiền thanh toán phải > 0!', 'danger')
            return redirect(url_for('invoices.payment_invoice', id=invoice.id))
        
        remaining = invoice.remaining_amount
        if amount > remaining:
            flash(f'⚠️ Số tiền thanh toán ({amount:,.0f}đ) lớn hơn số tiền còn nợ ({remaining:,.0f}đ)!', 'danger')
            return redirect(url_for('invoices.payment_invoice', id=invoice.id))
        
        # Parse payment date
        try:
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
        except:
            payment_date = datetime.now()
        
        # Tạo payment mới
        payment = Payment(
            invoice_id=invoice.id,
            amount=amount,
            payment_method=payment_method,
            payment_date=payment_date,
            notes=notes
        )
        
        db.session.add(payment)
        
        # Cập nhật trạng thái hóa đơn
        invoice.update_status()
        
        db.session.commit()
        
        flash(f'✅ Đã ghi nhận thanh toán {amount:,.0f}đ!', 'success')
        return redirect(url_for('invoices.view_invoice', id=invoice.id))
    
    # GET: Hiển thị form
    return render_template('invoices/payment.html', invoice=invoice, now=datetime.now())


# ============================================
# 6. XÓA HÓA ĐƠN
# ============================================
@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_invoice(id):
    """
    Xóa hóa đơn (chỉ cho phép nếu chưa có thanh toán)
    """
    invoice = Invoice.query.get_or_404(id)
    
    # Kiểm tra đã có thanh toán chưa
    if invoice.paid_amount > 0:
        flash('⚠️ Không thể xóa hóa đơn đã có thanh toán!', 'danger')
        return redirect(url_for('invoices.view_invoice', id=invoice.id))
    
    room_number = invoice.room.room_number
    month = invoice.month
    year = invoice.year
    
    db.session.delete(invoice)
    db.session.commit()
    
    flash(f'✅ Đã xóa hóa đơn phòng {room_number} tháng {month}/{year}!', 'success')
    return redirect(url_for('invoices.list_invoices'))


# ============================================
# 7. TẠO HÓA ĐƠN HÀNG LOẠT
# ============================================
@bp.route('/create-bulk', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def create_bulk_invoices():
    """
    Tạo hóa đơn cho tất cả phòng đang cho thuê
    Tiết kiệm thời gian đầu tháng
    """
    if request.method == 'POST':
        month = request.form.get('month', type=int)
        year = request.form.get('year', type=int)
        
        # Lấy đơn giá
        electric_unit_price = request.form.get('electric_unit_price', 3500, type=float)
        water_unit_price = request.form.get('water_unit_price', 20000, type=float)
        other_fees = request.form.get('other_fees', 0, type=float)
        
        # Lấy tất cả phòng đang cho thuê
        occupied_rooms = Room.query.filter_by(status='occupied').all()
        
        created_count = 0
        skipped_count = 0
        
        for room in occupied_rooms:
            # Kiểm tra đã tồn tại chưa
            existing = Invoice.query.filter_by(room_id=room.id, month=month, year=year).first()
            if existing:
                skipped_count += 1
                continue
            
            # Tạo hóa đơn mới
            invoice = Invoice(
                room_id=room.id,
                month=month,
                year=year,
                room_price=room.price,
                electric_old=0,
                electric_new=0,
                electric_unit_price=electric_unit_price,
                water_old=0,
                water_new=0,
                water_unit_price=water_unit_price,
                other_fees=other_fees,
                created_by=current_user.id,
                due_date=datetime.now() + timedelta(days=7)
            )
            
            invoice.calculate_total()
            db.session.add(invoice)
            created_count += 1
        
        db.session.commit()
        
        flash(f'✅ Đã tạo {created_count} hóa đơn, bỏ qua {skipped_count} hóa đơn đã tồn tại!', 'success')
        return redirect(url_for('invoices.list_invoices'))
    
    # GET: Hiển thị form
    now = datetime.now()
    occupied_rooms = Room.query.filter_by(status='occupied').order_by(Room.room_number).all()
    
    # Lấy tháng hiện tại để kiểm tra
    current_month = now.month
    current_year = now.year
    
    # Đếm số phòng chưa có hóa đơn trong tháng hiện tại
    rooms_without_invoice = []
    for room in occupied_rooms:
        existing = Invoice.query.filter_by(
            room_id=room.id, 
            month=current_month, 
            year=current_year
        ).first()
        if not existing:
            rooms_without_invoice.append(room)
    
    return render_template('invoices/create_bulk.html',
                         rooms=occupied_rooms,
                         rooms_without_invoice=rooms_without_invoice,
                         current_month=current_month,
                         current_year=current_year)
