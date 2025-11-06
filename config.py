import os
from dotenv import load_dotenv

# Lấy đường dẫn thư mục gốc
basedir = os.path.abspath(os.path.dirname(__file__))

# Load biến từ file .env
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Class chứa các cấu hình cho ứng dụng"""
    
    # Secret Key - Dùng để mã hóa session, cookie
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this'
    
    # Database URL - Đường dẫn đến database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'roommaster.db')
    
    # Tắt track modifications (tiết kiệm bộ nhớ)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Số item mỗi trang (phân trang)
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE') or 10)
    
    # Thư mục upload file
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    
    # Giới hạn kích thước file upload (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
