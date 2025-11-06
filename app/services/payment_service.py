"""
Payment Service - Business logic cho quản lý thanh toán
"""
from app import db
from app.models import Payment, Invoice
from datetime import datetime


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
                db.extract('month', Payment.payment_date) == month,
                db.extract('year', Payment.payment_date) == year
            )
        elif year:
            query = query.filter(
                db.extract('year', Payment.payment_date) == year
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
