"""
Security enhancements for RoomMaster
"""
from functools import wraps
from flask import request, abort
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Simple rate limiting (for production, use Flask-Limiter with Redis)
_rate_limit_storage = {}

def rate_limit(limit=5, per=60):
    """
    Simple rate limiting decorator
    Usage: @rate_limit(limit=5, per=60) # 5 requests per 60 seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            
            # Get current time
            now = datetime.utcnow()
            
            # Initialize storage for this IP
            if client_ip not in _rate_limit_storage:
                _rate_limit_storage[client_ip] = []
            
            # Clean old requests
            _rate_limit_storage[client_ip] = [
                req_time for req_time in _rate_limit_storage[client_ip]
                if now - req_time < timedelta(seconds=per)
            ]
            
            # Check limit
            if len(_rate_limit_storage[client_ip]) >= limit:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                abort(429)  # Too Many Requests
            
            # Add current request
            _rate_limit_storage[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_file_extension(filename, allowed_extensions):
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks
    """
    import os
    from werkzeug.utils import secure_filename
    
    # Use werkzeug's secure_filename
    safe_name = secure_filename(filename)
    
    # Remove any remaining path separators
    safe_name = safe_name.replace('/', '').replace('\\', '')
    
    return safe_name


def add_security_headers(response):
    """
    Add security headers to response
    Call this in app/__init__.py: @app.after_request
    """
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Strict Transport Security (only for HTTPS)
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = \
        "default-src 'self'; " \
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " \
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " \
        "font-src 'self' https://cdn.jsdelivr.net; " \
        "img-src 'self' data: https:; " \
        "connect-src 'self' https://cdn.jsdelivr.net; "
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response


def validate_password_strength(password):
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"
    
    if not any(c.isupper() for c in password):
        return False, "Mật khẩu phải có ít nhất 1 chữ hoa"
    
    if not any(c.islower() for c in password):
        return False, "Mật khẩu phải có ít nhất 1 chữ thường"
    
    if not any(c.isdigit() for c in password):
        return False, "Mật khẩu phải có ít nhất 1 số"
    
    return True, ""


def log_security_event(event_type, details, ip_address=None):
    """
    Log security-related events
    """
    if ip_address is None:
        ip_address = request.remote_addr if request else 'unknown'
    
    logger.warning(
        f"SECURITY EVENT: {event_type} | "
        f"IP: {ip_address} | "
        f"Details: {details}"
    )
