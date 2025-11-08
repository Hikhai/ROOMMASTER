from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Khởi tạo các extension (tạm thời chưa gắn vào app)
db = SQLAlchemy()                    # Quản lý database
login_manager = LoginManager()       # Quản lý đăng nhập
migrate = Migrate()                  # Quản lý migration database


def create_app(config_class=Config):
    """
    Factory function - Tạo và cấu hình Flask app
    
    Lợi ích: 
    - Dễ test (tạo nhiều app với config khác nhau)
    - Tránh circular import
    - Tách biệt concerns
    """
    
    # Tạo Flask app
    app = Flask(__name__)
    
    # Load cấu hình từ class Config
    app.config.from_object(config_class)
    
    # Gắn extensions vào app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Cấu hình Login Manager
    login_manager.login_view = 'auth.login'  # Redirect đến trang login nếu chưa đăng nhập
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'warning'  # Bootstrap alert class
    
    # Setup logging
    from app.utils.logger import setup_logging
    setup_logging(app)
    
    # Import models (phải import sau khi khởi tạo db)
    from app import models
    
    # Đăng ký blueprints (routes)
    from app.routes import auth, main, rooms, tenants, invoices, reports, users, services
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(tenants.bp)
    app.register_blueprint(invoices.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(services.bp)
    
    # Đăng ký error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Add security headers
    from app.security import add_security_headers
    @app.after_request
    def security_headers(response):
        return add_security_headers(response)
    
    # Đăng ký template filters
    from app.utils.helpers import format_currency, format_date, get_status_badge_class
    app.jinja_env.filters['currency'] = format_currency
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['status_badge'] = get_status_badge_class
    
    # Tạo bảng database nếu chưa tồn tại
    with app.app_context():
        db.create_all()
    
    app.logger.info('RoomMaster application started successfully')
    
    return app
