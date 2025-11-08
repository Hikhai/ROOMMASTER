from flask import Blueprint, render_template, request
from flask_login import login_required
from app import db
from app.models import Invoice, Room, Tenant, Payment
from app.services.payment_service import PaymentService
from sqlalchemy import func, extract
from datetime import datetime

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/')
@login_required
def index():
    """Reports overview"""
    return render_template('reports/index.html')


@bp.route('/revenue')
@login_required
def revenue():
    """Revenue report"""
    year = request.args.get('year', datetime.now().year, type=int)
    
    # Monthly revenue
    monthly_data = db.session.query(
        Invoice.month,
        func.sum(Invoice.total_amount).label('total'),
        func.count(Invoice.id).label('count')
    ).filter(
        Invoice.year == year,
        Invoice.status == 'paid'
    ).group_by(Invoice.month).all()
    
    # Prepare data for chart
    months = list(range(1, 13))
    revenue_data = {m: 0 for m in months}
    invoice_count = {m: 0 for m in months}
    
    for month, total, count in monthly_data:
        revenue_data[month] = float(total)
        invoice_count[month] = count
    
    total_revenue = sum(revenue_data.values())
    total_invoices = sum(invoice_count.values())
    
    return render_template('reports/revenue.html',
                         year=year,
                         revenue_data=revenue_data,
                         invoice_count=invoice_count,
                         total_revenue=total_revenue,
                         total_invoices=total_invoices)


@bp.route('/occupancy')
@login_required
def occupancy():
    """Room occupancy report"""
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(status='occupied').count()
    available_rooms = Room.query.filter_by(status='available').count()
    maintenance_rooms = Room.query.filter_by(status='maintenance').count()
    
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Rooms by floor
    rooms_by_floor = db.session.query(
        Room.floor,
        func.count(Room.id).label('count')
    ).group_by(Room.floor).all()
    
    return render_template('reports/occupancy.html',
                         total_rooms=total_rooms,
                         occupied_rooms=occupied_rooms,
                         available_rooms=available_rooms,
                         maintenance_rooms=maintenance_rooms,
                         occupancy_rate=occupancy_rate,
                         rooms_by_floor=rooms_by_floor)


@bp.route('/tenants')
@login_required
def tenants():
    """Tenant statistics"""
    total_tenants = Tenant.query.count()
    active_tenants = Tenant.query.filter_by(status='active').count()
    moved_out_tenants = Tenant.query.filter_by(status='moved_out').count()
    
    # Recent move-ins
    recent_move_ins = Tenant.query.filter_by(status='active').order_by(
        Tenant.move_in_date.desc()
    ).limit(10).all()
    
    return render_template('reports/tenants.html',
                         total_tenants=total_tenants,
                         active_tenants=active_tenants,
                         moved_out_tenants=moved_out_tenants,
                         recent_move_ins=recent_move_ins)


@bp.route('/overdue')
@login_required
def overdue():
    """
    Báo cáo công nợ chi tiết
    Phân loại theo mức độ: warning (1-5 ngày), danger (5-10 ngày), critical (>10 ngày)
    """
    month = request.args.get('month', type=int)
    year = request.args.get('year', datetime.now().year, type=int)
    
    # Lấy báo cáo công nợ từ PaymentService
    debt_report = PaymentService.get_debt_report(month=month, year=year)
    
    # Lấy tổng hợp thu tiền
    collection_summary = PaymentService.get_collection_summary(month=month, year=year)
    
    return render_template('reports/overdue.html',
                         debt_report=debt_report,
                         collection_summary=collection_summary,
                         month=month,
                         year=year,
                         now=datetime.now())

