# 🚀 HƯỚNG DẪN TRIỂN KHAI PRODUCTION

## 📋 MỤC LỤC
1. [Chuẩn bị](#chuẩn-bị)
2. [Tối ưu hóa](#tối-ưu-hóa)
3. [Deploy lên VPS/Server](#deploy-lên-vpsserver)
4. [Deploy lên PythonAnywhere](#deploy-lên-pythonanywhere)
5. [Deploy lên Heroku](#deploy-lên-heroku)
6. [Bảo mật](#bảo-mật)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🔧 CHUẨN BỊ

### 1. Kiểm tra code

```bash
# Test tất cả chức năng
python run.py

# Check errors
flask init-db
flask seed-db
```

### 2. Cập nhật requirements.txt

```bash
pip freeze > requirements.txt
```

### 3. Cấu hình môi trường

```bash
# Copy và chỉnh sửa .env
cp .env.example .env

# Thay đổi:
FLASK_ENV=production
SECRET_KEY=<generate-strong-key>
DATABASE_URL=<production-database-url>
```

**Tạo SECRET_KEY mạnh:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ⚡ TỐI ƯU HÓA

### 1. Tối ưu database

```bash
python optimize_production.py
```

Script này sẽ:
- ✅ Thêm indexes cho queries nhanh hơn
- ✅ Optimize SQLite (WAL mode, cache)
- ✅ Analyze database statistics

### 2. Minify static files

```bash
python minify_static.py
```

Script này sẽ:
- ✅ Minify CSS (giảm ~30-40% size)
- ✅ Minify JavaScript (giảm ~20-30% size)
- ✅ Tạo files .min.css và .min.js

**Cập nhật templates:**
```html
<!-- Development -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<!-- Production -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.min.css') }}">
```

### 3. Xóa files không cần thiết

```bash
# Xóa cache
rm -rf __pycache__ app/__pycache__
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Xóa logs cũ
rm -rf logs/*

# Xóa database development (nếu có)
# rm roommaster.db
```

---

## 🖥️ DEPLOY LÊN VPS/SERVER

### Chuẩn bị server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install PostgreSQL (recommended)
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install supervisor
sudo apt install supervisor -y
```

### Setup project

```bash
# Tạo user riêng
sudo useradd -m -s /bin/bash roommaster
sudo su - roommaster

# Clone project
git clone https://github.com/yourusername/roommaster.git
cd roommaster

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Cấu hình .env
nano .env
```

### Cấu hình PostgreSQL

```bash
# Login PostgreSQL
sudo -u postgres psql

# Tạo database và user
CREATE DATABASE roommaster_db;
CREATE USER roommaster_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE roommaster_db TO roommaster_user;
\q

# Cập nhật DATABASE_URL trong .env
DATABASE_URL=postgresql://roommaster_user:strong-password@localhost/roommaster_db
```

### Khởi tạo database

```bash
# Activate venv
source venv/bin/activate

# Init database
python optimize_production.py
python seed_data.py  # Nếu cần data mẫu
```

### Cấu hình Gunicorn

Tạo file `gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/home/roommaster/roommaster/logs/gunicorn_error.log"
accesslog = "/home/roommaster/roommaster/logs/gunicorn_access.log"
loglevel = "info"
```

Test Gunicorn:
```bash
gunicorn -c gunicorn_config.py run:app
```

### Cấu hình Supervisor

Tạo file `/etc/supervisor/conf.d/roommaster.conf`:
```ini
[program:roommaster]
directory=/home/roommaster/roommaster
command=/home/roommaster/roommaster/venv/bin/gunicorn -c gunicorn_config.py run:app
user=roommaster
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/home/roommaster/roommaster/logs/supervisor_error.log
stdout_logfile=/home/roommaster/roommaster/logs/supervisor_access.log
```

Start service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start roommaster
sudo supervisorctl status roommaster
```

### Cấu hình Nginx

Tạo file `/etc/nginx/sites-available/roommaster`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/roommaster/roommaster/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 16M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/roommaster /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Cài đặt SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 🐍 DEPLOY LÊN PYTHONANYWHERE

### 1. Đăng ký tài khoản
- Truy cập: https://www.pythonanywhere.com
- Đăng ký tài khoản Free/Paid

### 2. Upload code

**Cách 1: Git**
```bash
cd ~
git clone https://github.com/yourusername/roommaster.git
```

**Cách 2: Upload files**
- Dashboard → Files → Upload files

### 3. Cài đặt virtualenv

```bash
cd roommaster
mkvirtualenv --python=/usr/bin/python3.10 roommaster-venv
pip install -r requirements.txt
```

### 4. Cấu hình .env

```bash
nano .env
```

### 5. Khởi tạo database

```bash
workon roommaster-venv
python optimize_production.py
python seed_data.py
```

### 6. Cấu hình Web App

Dashboard → Web → Add a new web app:

**WSGI configuration file:**
```python
import sys
import os

# Add project directory
project_home = '/home/yourusername/roommaster'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import app
from run import app as application
```

**Static files:**
- URL: `/static/`
- Directory: `/home/yourusername/roommaster/app/static/`

### 7. Reload web app

Dashboard → Web → Reload

---

## 🌐 DEPLOY LÊN HEROKU

### 1. Chuẩn bị files

**Procfile:**
```
web: gunicorn run:app
```

**runtime.txt:**
```
python-3.10.12
```

**Cập nhật requirements.txt:**
```bash
pip install gunicorn psycopg2-binary
pip freeze > requirements.txt
```

### 2. Deploy

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Tạo app
heroku create roommaster-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku main

# Khởi tạo database
heroku run python optimize_production.py
heroku run python seed_data.py

# Mở app
heroku open
```

---

## 🔒 BẢO MẬT

### Checklist bảo mật

- [ ] Thay đổi SECRET_KEY mạnh
- [ ] Không commit .env vào Git
- [ ] Sử dụng HTTPS (SSL certificate)
- [ ] Bật CSRF protection (đã có)
- [ ] Security headers (đã có trong app/security.py)
- [ ] Giới hạn file upload size
- [ ] Validate user input
- [ ] Rate limiting cho login
- [ ] Backup database định kỳ

### Tạo admin account an toàn

```python
# Trong Flask shell
flask shell

>>> from app.models import User
>>> from app import db
>>> admin = User(username='admin', email='admin@company.com', full_name='Admin', role='admin')
>>> admin.set_password('VeryStrongPassword123!')
>>> db.session.add(admin)
>>> db.session.commit()
```

---

## 📊 MONITORING & MAINTENANCE

### Backup database

**PostgreSQL:**
```bash
# Backup
pg_dump -U roommaster_user roommaster_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U roommaster_user roommaster_db < backup_20251108.sql
```

**SQLite:**
```bash
# Backup
cp roommaster.db roommaster_backup_$(date +%Y%m%d).db
```

### Xem logs

```bash
# Application logs
tail -f logs/roommaster.log

# Gunicorn logs
tail -f logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Cập nhật code

```bash
# Pull code mới
cd /home/roommaster/roommaster
git pull

# Activate venv
source venv/bin/activate

# Install new dependencies
pip install -r requirements.txt

# Restart app
sudo supervisorctl restart roommaster
```

### Monitoring tools

**Tích hợp Sentry (Error tracking):**
```bash
pip install sentry-sdk[flask]
```

```python
# Trong app/__init__.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FlaskIntegration()]
)
```

---

## 🎯 CHECKLIST TRƯỚC KHI DEPLOY

### Development
- [ ] Test tất cả chức năng
- [ ] Fix all bugs
- [ ] Optimize queries
- [ ] Minify static files

### Configuration
- [ ] Set FLASK_ENV=production
- [ ] Generate strong SECRET_KEY
- [ ] Configure production database
- [ ] Update .env variables

### Security
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookies
- [ ] Add security headers
- [ ] Rate limiting
- [ ] Input validation

### Optimization
- [ ] Add database indexes
- [ ] Enable caching
- [ ] Compress static files
- [ ] CDN for static files (optional)

### Monitoring
- [ ] Setup error logging
- [ ] Configure backups
- [ ] Setup monitoring tools
- [ ] Test recovery procedures

---

## 📞 HỖ TRỢ

- **Documentation:** README.md, GUIDE.md
- **Troubleshooting:** Check logs first
- **Database issues:** Run optimize_production.py
- **Performance:** Check database indexes, enable caching

---

**Chúc bạn deploy thành công! 🎉**
