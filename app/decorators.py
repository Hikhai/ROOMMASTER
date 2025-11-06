"""
Decorators for access control and permissions
"""
from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def admin_required(f):
    """
    Decorator yêu cầu user phải có role 'admin'
    Sử dụng: @admin_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'admin':
            flash('Bạn không có quyền truy cập chức năng này.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def require_role(*roles):
    """
    Decorator yêu cầu user phải có một trong các role được chỉ định
    Sử dụng: @require_role('admin', 'manager')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('Bạn không có quyền truy cập chức năng này.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def manager_or_admin(f):
    """
    Decorator cho phép admin và manager
    Sử dụng: @manager_or_admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role not in ['admin', 'manager']:
            flash('Bạn không có quyền thực hiện thao tác này. (Chỉ Admin/Manager)', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
