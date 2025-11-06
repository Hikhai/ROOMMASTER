"""
Utility Helpers - Các hàm tiện ích dùng chung
"""
from datetime import datetime
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def format_currency(amount):
    """
    Format số tiền theo định dạng Việt Nam
    
    Args:
        amount: Số tiền
        
    Returns:
        String đã format (VD: 1.000.000 đ)
    """
    if amount is None:
        return '0 đ'
    return f"{amount:,.0f} đ".replace(',', '.')


def format_date(date_obj, format_str='%d/%m/%Y'):
    """
    Format date object thành string
    
    Args:
        date_obj: Date/datetime object
        format_str: Format string (mặc định dd/mm/yyyy)
        
    Returns:
        String đã format hoặc '-' nếu None
    """
    if not date_obj:
        return '-'
    
    if isinstance(date_obj, str):
        return date_obj
    
    return date_obj.strftime(format_str)


def parse_date(date_str, format_str='%d/%m/%Y'):
    """
    Parse string thành date object
    
    Args:
        date_str: String ngày tháng
        format_str: Format string (mặc định dd/mm/yyyy)
        
    Returns:
        Date object hoặc None nếu lỗi
    """
    if not date_str:
        return None
    
    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError:
        return None


def get_current_month_year():
    """
    Lấy tháng và năm hiện tại
    
    Returns:
        Tuple (month, year)
    """
    now = datetime.now()
    return now.month, now.year


def calculate_days_overdue(due_date):
    """
    Tính số ngày quá hạn
    
    Args:
        due_date: Date object
        
    Returns:
        Số ngày quá hạn (0 nếu chưa quá hạn)
    """
    if not due_date:
        return 0
    
    today = datetime.now().date()
    if due_date >= today:
        return 0
    
    return (today - due_date).days


def requires_role(*roles):
    """
    Decorator kiểm tra quyền truy cập
    
    Args:
        roles: Danh sách các role được phép truy cập
        
    Usage:
        @requires_role('admin', 'manager')
        def admin_only_view():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Vui lòng đăng nhập để truy cập', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('Bạn không có quyền truy cập chức năng này', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def paginate_query(query, page, per_page):
    """
    Phân trang cho query
    
    Args:
        query: SQLAlchemy query
        page: Trang hiện tại
        per_page: Số item mỗi trang
        
    Returns:
        Pagination object
    """
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def safe_int(value, default=0):
    """
    Chuyển đổi giá trị sang int an toàn
    
    Args:
        value: Giá trị cần chuyển đổi
        default: Giá trị mặc định nếu lỗi
        
    Returns:
        Integer
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """
    Chuyển đổi giá trị sang float an toàn
    
    Args:
        value: Giá trị cần chuyển đổi
        default: Giá trị mặc định nếu lỗi
        
    Returns:
        Float
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def get_status_badge_class(status):
    """
    Lấy class Bootstrap badge cho status
    
    Args:
        status: Trạng thái
        
    Returns:
        String class name
    """
    status_map = {
        'paid': 'success',
        'unpaid': 'danger',
        'partial': 'warning',
        'active': 'success',
        'moved_out': 'secondary',
        'available': 'success',
        'occupied': 'danger',
        'maintenance': 'warning'
    }
    return status_map.get(status, 'secondary')


def chunk_list(lst, chunk_size):
    """
    Chia list thành các chunk nhỏ
    
    Args:
        lst: List cần chia
        chunk_size: Kích thước mỗi chunk
        
    Returns:
        Generator các chunks
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
