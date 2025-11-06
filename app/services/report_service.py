"""
Report Service - Business logic cho báo cáo thống kê
"""
from app import db
from app.models import Invoice, Payment, Room, Tenant
from datetime import datetime, timedelta
from sqlalchemy import extract, func


class ReportService:
    """Service xử lý logic nghiệp vụ liên quan đến báo cáo"""
    
    @staticmethod
    def get_revenue_report(year, month=None):
        """
        Báo cáo doanh thu
        
        Args:
            year: Năm
            month: Tháng (optional, nếu None thì báo cáo cả năm)
            
        Returns:
            Dictionary chứa dữ liệu báo cáo
        """
        if month:
            # Báo cáo theo tháng
            invoices = Invoice.query.filter_by(year=year, month=month).all()
            
            total_invoices = len(invoices)
            total_amount = sum(inv.total_amount for inv in invoices)
            paid_amount = sum(inv.paid_amount for inv in invoices)
            
            return {
                'period': f'{month:02d}/{year}',
                'total_invoices': total_invoices,
                'total_amount': total_amount,
                'paid_amount': paid_amount,
                'unpaid_amount': total_amount - paid_amount,
                'collection_rate': (paid_amount / total_amount * 100) if total_amount > 0 else 0
            }
        else:
            # Báo cáo cả năm, chia theo tháng
            monthly_data = []
            
            for m in range(1, 13):
                invoices = Invoice.query.filter_by(year=year, month=m).all()
                
                total_amount = sum(inv.total_amount for inv in invoices)
                paid_amount = sum(inv.paid_amount for inv in invoices)
                
                monthly_data.append({
                    'month': m,
                    'total_invoices': len(invoices),
                    'total_amount': total_amount,
                    'paid_amount': paid_amount,
                    'unpaid_amount': total_amount - paid_amount
                })
            
            # Tổng năm
            year_total = sum(m['total_amount'] for m in monthly_data)
            year_paid = sum(m['paid_amount'] for m in monthly_data)
            
            return {
                'year': year,
                'monthly_data': monthly_data,
                'total_amount': year_total,
                'paid_amount': year_paid,
                'unpaid_amount': year_total - year_paid,
                'collection_rate': (year_paid / year_total * 100) if year_total > 0 else 0
            }
    
    @staticmethod
    def get_occupancy_report():
        """
        Báo cáo tình hình sử dụng phòng
        
        Returns:
            Dictionary chứa dữ liệu báo cáo
        """
        total_rooms = Room.query.count()
        occupied_rooms = Room.query.filter_by(status='occupied').count()
        available_rooms = Room.query.filter_by(status='available').count()
        maintenance_rooms = Room.query.filter_by(status='maintenance').count()
        
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
        
        # Thống kê theo tầng
        floors_data = db.session.query(
            Room.floor,
            func.count(Room.id).label('total'),
            func.sum(func.case((Room.status == 'occupied', 1), else_=0)).label('occupied')
        ).group_by(Room.floor).order_by(Room.floor).all()
        
        floors = []
        for floor_data in floors_data:
            floor, total, occupied = floor_data
            floors.append({
                'floor': floor,
                'total': total,
                'occupied': occupied or 0,
                'available': total - (occupied or 0),
                'rate': ((occupied or 0) / total * 100) if total > 0 else 0
            })
        
        return {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'maintenance_rooms': maintenance_rooms,
            'occupancy_rate': occupancy_rate,
            'floors': floors
        }
    
    @staticmethod
    def get_overdue_report():
        """
        Báo cáo hóa đơn quá hạn
        
        Returns:
            Dictionary chứa dữ liệu báo cáo
        """
        today = datetime.now().date()
        
        overdue_invoices = Invoice.query.filter(
            Invoice.status.in_(['unpaid', 'partial']),
            Invoice.due_date < today
        ).order_by(Invoice.due_date).all()
        
        total_overdue = len(overdue_invoices)
        total_amount = sum(inv.remaining_amount for inv in overdue_invoices)
        
        # Phân loại theo độ trễ
        categories = {
            'under_7_days': [],
            '7_to_30_days': [],
            'over_30_days': []
        }
        
        for invoice in overdue_invoices:
            days_overdue = (today - invoice.due_date).days
            
            if days_overdue <= 7:
                categories['under_7_days'].append(invoice)
            elif days_overdue <= 30:
                categories['7_to_30_days'].append(invoice)
            else:
                categories['over_30_days'].append(invoice)
        
        return {
            'total_overdue': total_overdue,
            'total_amount': total_amount,
            'under_7_days': {
                'count': len(categories['under_7_days']),
                'amount': sum(inv.remaining_amount for inv in categories['under_7_days']),
                'invoices': categories['under_7_days']
            },
            '7_to_30_days': {
                'count': len(categories['7_to_30_days']),
                'amount': sum(inv.remaining_amount for inv in categories['7_to_30_days']),
                'invoices': categories['7_to_30_days']
            },
            'over_30_days': {
                'count': len(categories['over_30_days']),
                'amount': sum(inv.remaining_amount for inv in categories['over_30_days']),
                'invoices': categories['over_30_days']
            }
        }
    
    @staticmethod
    def get_tenant_report():
        """
        Báo cáo khách thuê
        
        Returns:
            Dictionary chứa dữ liệu báo cáo
        """
        total_tenants = Tenant.query.count()
        active_tenants = Tenant.query.filter_by(status='active').count()
        moved_out_tenants = Tenant.query.filter_by(status='moved_out').count()
        
        # Khách thuê mới trong 30 ngày
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        new_tenants = Tenant.query.filter(
            Tenant.move_in_date >= thirty_days_ago
        ).count()
        
        # Thống kê theo phòng
        rooms_with_tenants = db.session.query(
            Room.room_number,
            func.count(Tenant.id).label('tenant_count')
        ).join(Tenant, Room.id == Tenant.room_id)\
         .filter(Tenant.status == 'active')\
         .group_by(Room.id, Room.room_number)\
         .order_by(Room.room_number).all()
        
        return {
            'total_tenants': total_tenants,
            'active_tenants': active_tenants,
            'moved_out_tenants': moved_out_tenants,
            'new_tenants_30_days': new_tenants,
            'rooms_with_tenants': [
                {'room': room, 'count': count}
                for room, count in rooms_with_tenants
            ]
        }
    
    @staticmethod
    def get_dashboard_summary():
        """
        Tổng hợp dữ liệu cho dashboard
        
        Returns:
            Dictionary chứa dữ liệu tổng hợp
        """
        # Thống kê phòng
        total_rooms = Room.query.count()
        occupied_rooms = Room.query.filter_by(status='occupied').count()
        
        # Thống kê khách thuê
        active_tenants = Tenant.query.filter_by(status='active').count()
        
        # Thống kê hóa đơn tháng hiện tại
        now = datetime.now()
        current_month_invoices = Invoice.query.filter_by(
            month=now.month,
            year=now.year
        ).all()
        
        total_revenue = sum(inv.total_amount for inv in current_month_invoices)
        paid_revenue = sum(inv.paid_amount for inv in current_month_invoices)
        
        # Hóa đơn chưa thanh toán
        unpaid_invoices = Invoice.query.filter(
            Invoice.status.in_(['unpaid', 'partial'])
        ).count()
        
        return {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'occupancy_rate': (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0,
            'active_tenants': active_tenants,
            'total_revenue': total_revenue,
            'paid_revenue': paid_revenue,
            'unpaid_revenue': total_revenue - paid_revenue,
            'unpaid_invoices': unpaid_invoices
        }
