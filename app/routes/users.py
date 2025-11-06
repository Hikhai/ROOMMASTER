"""
User Management Routes - Chỉ Admin
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import User
from app.forms import RegisterForm
from app.decorators import admin_required

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
@admin_required
def list_users():
    """Danh sách nhân viên"""
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', 'all')
    
    # Query users
    query = User.query
    
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('users/list.html', 
                         users=users,
                         role_filter=role_filter)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """Thêm nhân viên mới"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data  # Admin chọn role
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Đã tạo tài khoản {user.username} thành công!', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/add.html', form=form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    """Sửa thông tin nhân viên"""
    user = User.query.get_or_404(id)
    
    # Truyền original username và email để bỏ qua validation
    form = RegisterForm(
        original_username=user.username,
        original_email=user.email,
        obj=user
    )
    
    # Xóa password khi GET (để form không hiện password cũ)
    if request.method == 'GET':
        form.password.data = ''
        form.password2.data = ''
    
    if form.validate_on_submit():
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.role = form.role.data
        
        # Chỉ đổi password nếu có nhập
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash(f'Đã cập nhật thông tin {user.username}!', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/edit.html', form=form, user=user)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    """Xóa nhân viên"""
    user = User.query.get_or_404(id)
    
    # Không cho xóa chính mình
    from flask_login import current_user
    if user.id == current_user.id:
        flash('Không thể xóa tài khoản của chính mình!', 'danger')
        return redirect(url_for('users.list_users'))
    
    # Kiểm tra xem user có dữ liệu liên quan không
    if user.invoices.count() > 0:
        flash(f'Không thể xóa {user.username} vì còn {user.invoices.count()} hóa đơn liên quan!', 'danger')
        return redirect(url_for('users.list_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Đã xóa tài khoản {username}!', 'success')
    return redirect(url_for('users.list_users'))


@bp.route('/<int:id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_password(id):
    """Reset mật khẩu về mặc định"""
    user = User.query.get_or_404(id)
    
    # Mật khẩu mặc định
    default_password = "123456"
    user.set_password(default_password)
    db.session.commit()
    
    flash(f'Đã reset mật khẩu của {user.username} về: {default_password}', 'warning')
    return redirect(url_for('users.list_users'))
