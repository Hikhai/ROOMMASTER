"""
Logging Configuration - Cấu hình logging cho ứng dụng
"""
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    """
    Thiết lập logging cho ứng dụng
    
    - Development: Log ra console
    - Production: Log ra file với rotation
    """
    
    # Nếu không phải debug mode, setup file logging
    if not app.debug and not app.testing:
        # Tạo thư mục logs nếu chưa tồn tại
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # File handler với rotation (10MB, giữ 10 file backup)
        file_handler = RotatingFileHandler(
            'logs/roommaster.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        
        # Format cho log
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        
        # Set level
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('RoomMaster startup')
    
    else:
        # Development mode - log ra console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('RoomMaster startup (Debug Mode)')


def get_logger(name):
    """
    Lấy logger instance
    
    Args:
        name: Tên logger (thường là __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
