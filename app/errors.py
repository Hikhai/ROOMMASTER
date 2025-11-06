"""
Error Handlers - Xử lý lỗi tập trung cho toàn bộ ứng dụng
"""
from flask import render_template, request, jsonify
from app import db
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Đăng ký các error handlers vào app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Bad Request - Yêu cầu không hợp lệ"""
        logger.warning(f'Bad Request: {request.url}')
        if request.is_json:
            return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(403)
    def forbidden(error):
        """Forbidden - Không có quyền truy cập"""
        logger.warning(f'Forbidden: {request.url}')
        if request.is_json:
            return jsonify({'error': 'Forbidden', 'message': 'Bạn không có quyền truy cập'}), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Not Found - Không tìm thấy trang"""
        logger.info(f'Not Found: {request.url}')
        if request.is_json:
            return jsonify({'error': 'Not Found', 'message': 'Không tìm thấy tài nguyên'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Internal Server Error - Lỗi server"""
        logger.error(f'Server Error: {request.url}', exc_info=True)
        db.session.rollback()  # Rollback transaction nếu có lỗi
        if request.is_json:
            return jsonify({'error': 'Internal Server Error', 'message': 'Đã xảy ra lỗi'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Xử lý tất cả các exception chưa được handle"""
        logger.error(f'Unhandled Exception: {request.url}', exc_info=True)
        db.session.rollback()
        
        # Trả về response tùy thuộc vào request type
        if request.is_json:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(error) if app.debug else 'Đã xảy ra lỗi'
            }), 500
        
        return render_template('errors/500.html', error=error if app.debug else None), 500
