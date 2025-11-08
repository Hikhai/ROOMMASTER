"""
Payment Service - Business logic cho quản lý thanh toán
"""
from app import db
from app.models import Payment, Invoice
from datetime import datetime
from sqlalchemy import func, extract


class PaymentService:
    """Service xử lý logic nghiệp vụ liên quan đến thanh toán"""
    
    @staticmethod
    def create_payment(invoice_id, data):
        """
        Tạo thanh toán mới
        
        Args:
            invoice_id: ID của hóa đơn
            data: Dictionary chứa thông tin thanh toán
            
        Returns:
            Payment object
        """
        try:
            invoice = Invoice.query.get_or_404(invoice_id)
            
            payment = Payment(
                invoice_id=invoice_id,
                amount=data['amount'],
                payment_method=data['payment_method'],
                payment_date=data['payment_date'],
                reference_number=data.get('reference_number'),
                notes=data.get('notes')
            )
            
            db.session.add(payment)
            
            # Cập nhật trạng thái hóa đơn
            invoice.update_status()
            
            db.session.commit()
            return payment
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_payment_by_id(payment_id):
        """Lấy thanh toán theo ID"""
        return Payment.query.get_or_404(payment_id)
    
    @staticmethod
    def update_payment(payment_id, data):
        """
        Cập nhật thanh toán
        
        Args:
            payment_id: ID của thanh toán
            data: Dictionary chứa thông tin cần update
            
        Returns:
            Payment object
        """
        try:
            payment = Payment.query.get_or_404(payment_id)
            
            for key, value in data.items():
                if hasattr(payment, key) and key not in ['id', 'invoice_id']:
                    setattr(payment, key, value)
            
            # Cập nhật lại trạng thái hóa đơn
            payment.invoice.update_status()
            
            db.session.commit()
            return payment
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_payment(payment_id):
        """
        Xóa thanh toán
        
        Args:
            payment_id: ID của thanh toán
            
        Returns:
            True nếu thành công
        """
        try:
            payment = Payment.query.get_or_404(payment_id)
            invoice = payment.invoice
            
            db.session.delete(payment)
            
            # Cập nhật lại trạng thái hóa đơn
            invoice.update_status()
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_payments_by_invoice(invoice_id):
        """Lấy danh sách thanh toán của một hóa đơn"""
        return Payment.query.filter_by(invoice_id=invoice_id)\
            .order_by(Payment.payment_date.desc()).all()
    
    @staticmethod
    def get_payment_statistics(month=None, year=None):
        """
        Thống kê thanh toán
        
        Args:
            month: Tháng (optional)
            year: Năm (optional)
            
        Returns:
            Dictionary chứa thống kê
        """
        query = Payment.query
        
        if month and year:
            query = query.filter(
                extract('month', Payment.payment_date) == month,
                extract('year', Payment.payment_date) == year
            )
        elif year:
            query = query.filter(
                extract('year', Payment.payment_date) == year
            )
        
        payments = query.all()
        
        total_payments = len(payments)
        total_amount = sum(p.amount for p in payments)
        
        # Thống kê theo phương thức
        by_method = {}
        for payment in payments:
            method = payment.payment_method
            if method not in by_method:
                by_method[method] = {'count': 0, 'amount': 0}
            by_method[method]['count'] += 1
            by_method[method]['amount'] += payment.amount
        
        return {
            'total_payments': total_payments,
            'total_amount': total_amount,
            'by_method': by_method
        }
    
    @staticmethod
    def get_debt_report(month=None, year=None):
        """
        Báo cáo công nợ chi tiết
        
        Args:
            month: Tháng (optional)
            year: Năm (optional)
            
        Returns:
            Dictionary chứa thông tin công nợ
        """
        query = Invoice.query
        
        if month and year:
            query = query.filter_by(month=month, year=year)
        elif year:
            query = query.filter_by(year=year)
        
        invoices = query.all()
        
        # Phân loại hóa đơn
        paid_invoices = []
        partial_invoices = []
        unpaid_invoices = []
        overdue_warning = []  # 1-5 ngày
        overdue_danger = []   # 5-10 ngày
        overdue_critical = [] # >10 ngày
        
        total_amount = 0
        total_paid = 0
        total_remaining = 0
        
        for invoice in invoices:
            total_amount += invoice.total_amount
            total_paid += invoice.paid_amount
            total_remaining += invoice.remaining_amount
            
            if invoice.status == 'paid':
                paid_invoices.append(invoice)
            elif invoice.status == 'partial':
                partial_invoices.append(invoice)
            else:
                unpaid_invoices.append(invoice)
            
            # Phân loại quá hạn
            if invoice.status != 'paid':
                level = invoice.overdue_level
                if level == 'warning':
                    overdue_warning.append(invoice)
                elif level == 'danger':
                    overdue_danger.append(invoice)
                elif level == 'critical':
                    overdue_critical.append(invoice)
        
        return {
            'total_invoices': len(invoices),
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_remaining': total_remaining,
            'paid_invoices': paid_invoices,
            'paid_count': len(paid_invoices),
            'partial_invoices': partial_invoices,
            'partial_count': len(partial_invoices),
            'unpaid_invoices': unpaid_invoices,
            'unpaid_count': len(unpaid_invoices),
            'overdue_warning': overdue_warning,
            'overdue_warning_count': len(overdue_warning),
            'overdue_warning_amount': sum(inv.remaining_amount for inv in overdue_warning),
            'overdue_danger': overdue_danger,
            'overdue_danger_count': len(overdue_danger),
            'overdue_danger_amount': sum(inv.remaining_amount for inv in overdue_danger),
            'overdue_critical': overdue_critical,
            'overdue_critical_count': len(overdue_critical),
            'overdue_critical_amount': sum(inv.remaining_amount for inv in overdue_critical),
        }
    
    @staticmethod
    def get_collection_summary(month=None, year=None):
        """
        Tổng hợp thu tiền trong kỳ
        
        Args:
            month: Tháng (optional)
            year: Năm (optional)
            
        Returns:
            Dictionary chứa tổng hợp thu tiền
        """
        invoice_query = Invoice.query
        
        if month and year:
            invoice_query = invoice_query.filter_by(month=month, year=year)
        elif year:
            invoice_query = invoice_query.filter_by(year=year)
        
        invoices = invoice_query.all()
        
        # Tổng phải thu
        total_receivable = sum(inv.total_amount for inv in invoices)
        
        # Tổng đã thu
        total_collected = sum(inv.paid_amount for inv in invoices)
        
        # Tổng chưa thu
        total_uncollected = sum(inv.remaining_amount for inv in invoices)
        
        # Tỷ lệ thu
        collection_rate = (total_collected / total_receivable * 100) if total_receivable > 0 else 0
        
        return {
            'total_receivable': total_receivable,
            'total_collected': total_collected,
            'total_uncollected': total_uncollected,
            'collection_rate': collection_rate,
            'invoice_count': len(invoices)
        }

