from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Room, Tenant
from app.forms import RoomForm
from app.decorators import manager_or_admin, admin_required

bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# ============================================
# ROUTE 1: DANH SÁCH PHÒNG
# ============================================
@bp.route('/')
@login_required
def list_rooms():
    """
    Hiển thị danh sách tất cả phòng
    Hỗ trợ tìm kiếm và lọc theo trạng thái
    """
    
    # Lấy tham số tìm kiếm từ URL (?search=P101)
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    # Query cơ bản
    query = Room.query
    
    # Tìm kiếm theo số phòng
    if search:
        query = query.filter(Room.room_number.like(f'%{search}%'))
    
    # Lọc theo trạng thái
    if status_filter:
        query = query.filter(Room.status == status_filter)
    
    # Sắp xếp theo số phòng
    rooms = query.order_by(Room.room_number).all()
    
    return render_template('rooms/list.html', 
                         rooms=rooms, 
                         search=search,
                         status_filter=status_filter)


# ============================================
# ROUTE 2: THÊM PHÒNG MỚI
# ============================================
@bp.route('/add', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def add_room():
    """
    Hiển thị form thêm phòng và xử lý submit
    """
    form = RoomForm()
    
    if form.validate_on_submit():
        # Kiểm tra số phòng đã tồn tại chưa
        existing_room = Room.query.filter_by(room_number=form.room_number.data).first()
        if existing_room:
            flash(f'Phòng {form.room_number.data} đã tồn tại!', 'danger')
            return render_template('rooms/add.html', form=form)
        
        # Tạo phòng mới
        room = Room(
            room_number=form.room_number.data,
            floor=form.floor.data,
            area=form.area.data,
            price=form.price.data,
            status=form.status.data,
            description=form.description.data
        )
        
        # Lưu vào database
        db.session.add(room)
        db.session.commit()
        
        flash(f'Đã thêm phòng {room.room_number} thành công!', 'success')
        return redirect(url_for('rooms.list_rooms'))
    
    return render_template('rooms/add.html', form=form)


# ============================================
# ROUTE 3: SỬA PHÒNG
# ============================================
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@manager_or_admin
def edit_room(id):
    """
    Chỉnh sửa thông tin phòng
    """
    # Lấy phòng từ database (hoặc 404 nếu không tồn tại)
    room = Room.query.get_or_404(id)
    
    # Truyền original_room_number để bỏ qua validation
    form = RoomForm(original_room_number=room.room_number, obj=room)
    
    if form.validate_on_submit():
        # Kiểm tra logic trạng thái phòng
        new_status = form.status.data
        
        # Nếu đổi thành "occupied" (đã thuê), phải có khách thuê đang ở
        if new_status == 'occupied':
            active_tenant = room.tenants.filter_by(status='active').first()
            if not active_tenant:
                flash(f'Không thể đổi trạng thái thành "Đã thuê" vì phòng chưa có khách thuê!', 'danger')
                return render_template('rooms/edit.html', form=form, room=room)
        
        # Nếu đổi thành "available" (trống), phải kiểm tra xem có khách đang ở không
        if new_status == 'available':
            active_tenant = room.tenants.filter_by(status='active').first()
            if active_tenant:
                flash(f'Không thể đổi trạng thái thành "Trống" vì phòng đang có khách thuê ({active_tenant.full_name})!', 'danger')
                return render_template('rooms/edit.html', form=form, room=room)
        
        # Cập nhật thông tin
        room.room_number = form.room_number.data
        room.floor = form.floor.data
        room.area = form.area.data
        room.price = form.price.data
        room.deposit = form.deposit.data
        room.status = form.status.data
        room.description = form.description.data
        
        db.session.commit()
        
        flash(f'Đã cập nhật phòng {room.room_number}!', 'success')
        return redirect(url_for('rooms.list_rooms'))
    
    return render_template('rooms/edit.html', form=form, room=room)


# ============================================
# ROUTE 4: XÓA PHÒNG  
# ============================================
@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete_room(id):
    """
    Xóa phòng khỏi hệ thống
    """
    room = Room.query.get_or_404(id)
    
    # Kiểm tra phòng có khách thuê không
    if room.tenants.filter_by(status='active').count() > 0:
        flash(f'Không thể xóa phòng {room.room_number} vì đang có khách thuê!', 'danger')
        return redirect(url_for('rooms.list_rooms'))
    
    # Kiểm tra phòng có hóa đơn không
    if room.invoices.count() > 0:
        flash(f'Không thể xóa phòng {room.room_number} vì đã có hóa đơn!', 'warning')
        return redirect(url_for('rooms.list_rooms'))
    
    # Xóa phòng
    room_number = room.room_number
    db.session.delete(room)
    db.session.commit()
    
    flash(f'Đã xóa phòng {room_number}!', 'success')
    return redirect(url_for('rooms.list_rooms'))


# ============================================
# ROUTE 5: CHI TIẾT PHÒNG (Bonus)
# ============================================
@bp.route('/detail/<int:id>')
@login_required
def detail_room(id):
    """
    Xem chi tiết phòng (khách thuê, lịch sử hóa đơn...)
    """
    room = Room.query.get_or_404(id)
    
    # Lấy khách thuê hiện tại
    current_tenant = room.tenants.filter_by(status='active').first()
    
    # Lấy 5 hóa đơn gần nhất (sắp xếp theo ngày tạo)
    from app.models import Invoice
    recent_invoices = room.invoices.order_by(
        Invoice.created_at.desc()
    ).limit(5).all()
    
    return render_template('rooms/detail.html', 
                         room=room,
                         current_tenant=current_tenant,
                         recent_invoices=recent_invoices)


# ============================================
# LEGACY ROUTES (giữ để tương thích ngược)
# ============================================
@bp.route('/index')
@login_required
def index():
    """Redirect to list_rooms"""
    return redirect(url_for('rooms.list_rooms'))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Redirect to add_room"""
    return redirect(url_for('rooms.add_room'))


@bp.route('/<int:id>')
@login_required
def detail(id):
    """Redirect to detail_room"""
    return redirect(url_for('rooms.detail_room', id=id))


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Redirect to edit_room"""
    return redirect(url_for('rooms.edit_room', id=id))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Redirect to delete_room"""
    return redirect(url_for('rooms.delete_room', id=id))
