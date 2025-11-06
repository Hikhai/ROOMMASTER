"""
Invoice Service - Business logic cho quản lý hóa đơn
"""
from app import db
from app.models import Invoice, Room, Service, Payment
from datetime import datetime, date
from sqlalchemy import and_, or_, extract


class InvoiceService:
    """Service xử lý logic nghiệp vụ liên quan đến hóa đơn"""
    
    @staticmethod
    def get_all_invoices(page=1, per_page=10, filters=None):
        """
        Lấy danh sách hóa đơn với filter và phân trang
        
        Args:
            page: Trang hiện tại
            per_page: Số hóa đơn mỗi trang
            filters: Dictionary chứa các bộ lọc (status, month, year, room_id)
            
        Returns:
            Pagination object
        """
        query = Invoice.query
        
        if filters:
            if 'status' in filters and filters['status']:
                query = query.filter(Invoice.status == filters['status'])
            
            if 'month' in filters and filters['month']:
                query = query.filter(Invoice.month == int(filters['month']))
            
            if 'year' in filters and filters['year']:
                query = query.filter(Invoice.year == int(filters['year']))
            
            if 'room_id' in filters and filters['room_id']:
                query = query.filter(Invoice.room_id == int(filters['room_id']))
        
        return query.order_by(Invoice.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        """Lấy hóa đơn theo ID"""
        return Invoice.query.get_or_404(invoice_id)
    
    @staticmethod
    def create_invoice(data):
        """
        Tạo hóa đơn mới
        
        Args:
            data: Dictionary chứa thông tin hóa đơn
            
        Returns:
            Invoice object
        """
        try:
            invoice = Invoice(
                room_id=data['room_id'],
                month=data['month'],
                year=data['year'],
                room_charge=data['room_charge'],
                due_date=data.get('due_date'),
                notes=data.get('notes'),
                status='unpaid'
            )
            db.session.add(invoice)
            db.session.commit()
            return invoice
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_bulk_invoices(month, year, room_ids, due_date=None):
        """
        Tạo hàng loạt hóa đơn cho nhiều phòng
        
        Args:
            month: Tháng
            year: Năm
            room_ids: List các room_id
            due_date: Hạn thanh toán
            
        Returns:
            Tuple (số hóa đơn tạo thành công, số hóa đơn bị lỗi)
        """
        success_count = 0
        error_count = 0
        
        for room_id in room_ids:
            try:
                # Kiểm tra đã tồn tại hóa đơn chưa
                existing = Invoice.query.filter_by(
                    room_id=room_id,
                    month=month,
                    year=year
                ).first()
                
                if existing:
                    error_count += 1
                    continue
                
                # Lấy thông tin phòng
                room = Room.query.get(room_id)
                if not room:
                    error_count += 1
                    continue
                
                # Tạo hóa đơn
                invoice = Invoice(
                    room_id=room_id,
                    month=month,
                    year=year,
                    room_charge=room.price,
                    due_date=due_date,
                    status='unpaid'
                )
                db.session.add(invoice)
                success_count += 1
                
            except Exception:
                error_count += 1
                continue
        
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        
        return success_count, error_count
    
    @staticmethod
    def update_invoice(invoice_id, data):
        """Cập nhật hóa đơn"""
        try:
            invoice = Invoice.query.get_or_404(invoice_id)
            
            for key, value in data.items():
                if hasattr(invoice, key) and key not in ['id', 'created_at']:
                    setattr(invoice, key, value)
            
            db.session.commit()
            return invoice
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_invoice(invoice_id):
        """Xóa hóa đơn"""
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # Xóa các payment liên quan
        Payment.query.filter_by(invoice_id=invoice_id).delete()
        
        try:
            db.session.delete(invoice)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_overdue_invoices():
        """Lấy danh sách hóa đơn quá hạn"""
        today = date.today()
        return Invoice.query.filter(
            and_(
                Invoice.status.in_(['unpaid', 'partial']),
                Invoice.due_date < today
            )
        ).all()
    
    @staticmethod
    def get_invoice_statistics(month=None, year=None):
        """
        Thống kê hóa đơn
        
        Args:
            month: Tháng (optional)
            year: Năm (optional)
            
        Returns:
            Dictionary chứa thống kê
        """
        query = Invoice.query
        
        if month and year:
            query = query.filter_by(month=month, year=year)
        elif year:
            query = query.filter_by(year=year)
        
        invoices = query.all()
        
        total = len(invoices)
        paid = sum(1 for inv in invoices if inv.status == 'paid')
        unpaid = sum(1 for inv in invoices if inv.status == 'unpaid')
        partial = sum(1 for inv in invoices if inv.status == 'partial')
        
        total_amount = sum(inv.total_amount for inv in invoices)
        paid_amount = sum(inv.paid_amount for inv in invoices)
        
        return {
            'total': total,
            'paid': paid,
            'unpaid': unpaid,
            'partial': partial,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'remaining_amount': total_amount - paid_amount
        }
    
    @staticmethod
    def get_rooms_without_invoice(month, year):
        """
        Lấy danh sách phòng chưa có hóa đơn trong tháng
        
        Args:
            month: Tháng
            year: Năm
            
        Returns:
            List các Room objects
        """
        # Lấy các room_id đã có hóa đơn
        existing_room_ids = db.session.query(Invoice.room_id).filter_by(
            month=month,
            year=year
        ).all()
        existing_room_ids = [r[0] for r in existing_room_ids]
        
        # Lấy các phòng chưa có hóa đơn và đang có người thuê
        return Room.query.filter(
            and_(
                Room.status == 'occupied',
                ~Room.id.in_(existing_room_ids)
            )
        ).order_by(Room.room_number).all()
