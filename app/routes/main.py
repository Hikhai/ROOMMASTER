from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models import Room, Tenant, Invoice
from sqlalchemy import func
from datetime import datetime

bp = Blueprint('main', __name__)


# ============================================
# ROUTE: DASHBOARD (Trang chủ)
# ============================================
@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard - Hiển thị tổng quan hệ thống
    - Thống kê phòng (tổng, đã thuê, trống)
    - Thống kê khách thuê
    - Thống kê hóa đơn (chưa thanh toán, quá hạn)
    - Tổng nợ
    - Doanh thu tháng
    """
    
    # ========== THỐNG KÊ PHÒNG ==========
    total_rooms = Room.query.count()  # Tổng số phòng
    rented_rooms = Room.query.filter_by(status='occupied').count()  # Phòng đã cho thuê
    empty_rooms = Room.query.filter_by(status='available').count()  # Phòng trống
    
    # Danh sách phòng trống (để hiển thị chi tiết nếu cần)
    empty_room_list = Room.query.filter_by(status='available').all()
    
    # ========== THỐNG KÊ KHÁCH THUÊ ==========
    total_tenants = Tenant.query.filter_by(status='active').count()
    
    # ========== THỐNG KÊ HÓA ĐƠN ==========
    # Hóa đơn chưa thanh toán (unpaid, partial)
    unpaid_invoices = Invoice.query.filter(Invoice.status.in_(['unpaid', 'partial'])).count()
    
    # Danh sách hóa đơn chưa thanh toán (để hiển thị chi tiết)
    unpaid_invoice_list = Invoice.query.filter(
        Invoice.status.in_(['unpaid', 'partial'])
    ).order_by(Invoice.year.desc(), Invoice.month.desc()).limit(10).all()
    
    # ========== TÍNH TỔNG NỢ ==========
    # Tính tổng nợ bằng Python (vì paid_amount là @property)
    all_unpaid_invoices = Invoice.query.filter(
        Invoice.status.in_(['unpaid', 'partial'])
    ).all()
    
    total_debt = sum(invoice.remaining_amount for invoice in all_unpaid_invoices)
    
    # ========== DOANH THU THÁNG HIỆN TẠI ==========
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Doanh thu = tổng tiền đã thanh toán (paid_amount từ Payment) trong tháng hiện tại
    # Lưu ý: Chỉ tính số tiền thực tế đã nhận, không phải total_amount
    invoices_this_month = Invoice.query.filter(
        Invoice.month == current_month,
        Invoice.year == current_year
    ).all()
    
    # Tính doanh thu từ tất cả payments của các hóa đơn trong tháng
    monthly_revenue = sum(invoice.paid_amount for invoice in invoices_this_month)
    
    # ========== HÓA ĐƠN MỚI NHẤT ==========
    recent_invoices = Invoice.query.order_by(
        Invoice.created_at.desc()
    ).limit(5).all()
    
    # Render template với tất cả dữ liệu
    return render_template('dashboard.html',
                         title='Dashboard',
                         total_rooms=total_rooms,
                         rented_rooms=rented_rooms,
                         empty_rooms=empty_rooms,
                         empty_room_list=empty_room_list,
                         total_tenants=total_tenants,
                         unpaid_invoices=unpaid_invoices,
                         unpaid_invoice_list=unpaid_invoice_list,
                         total_debt=total_debt,
                         monthly_revenue=monthly_revenue,
                         recent_invoices=recent_invoices,
                         now=datetime.now())


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
