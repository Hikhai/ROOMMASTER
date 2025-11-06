from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

# Tạo Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# ============================================
# ROUTE: ĐĂNG NHẬP
# ============================================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Xử lý đăng nhập
    GET: Hiển thị form
    POST: Xử lý submit form
    """
    
    # Nếu đã đăng nhập → Redirect về dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    # Khi user submit form
    if form.validate_on_submit():
        # Tìm user trong database
        user = User.query.filter_by(username=form.username.data).first()
        
        # Kiểm tra user và mật khẩu
        if user is None or not user.check_password(form.password.data):
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'danger')
            return redirect(url_for('auth.login'))
        
        # Đăng nhập thành công
        login_user(user, remember=form.remember_me.data)
        
        # Redirect về trang user muốn truy cập (hoặc dashboard)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        flash(f'Chào mừng {user.full_name}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Đăng nhập', form=form)



# ============================================
# ROUTE: ĐĂNG KÝ - ĐÃ TẮT (Internal app - chỉ admin tạo user)
# ============================================
# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     """DISABLED - Chỉ admin được tạo tài khoản qua User Management"""
#     flash('Chức năng đăng ký đã tắt. Vui lòng liên hệ admin để được cấp tài khoản.', 'warning')
#     return redirect(url_for('auth.login'))


# ============================================
# ROUTE: ĐĂNG XUẤT
# ============================================
@bp.route('/logout')
def logout():
    """Đăng xuất - Xóa session"""
    logout_user()
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('auth.login'))
