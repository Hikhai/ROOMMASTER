# 🆓 HƯỚNG DẪN DEPLOY MIỄN PHÍ ROOMMASTER

## 📋 CÁC NỀN TẢNG MIỄN PHÍ

| Platform | Database | Giới hạn | Khuyến nghị |
|----------|----------|----------|-------------|
| **PythonAnywhere** | SQLite/MySQL | 512MB disk | ⭐⭐⭐⭐⭐ Tốt nhất |
| **Render.com** | PostgreSQL | 512MB RAM | ⭐⭐⭐⭐ Rất tốt |
| **Railway.app** | PostgreSQL | 500h/tháng | ⭐⭐⭐⭐ Tốt |
| **Fly.io** | SQLite | 3GB persistent | ⭐⭐⭐ Khá |
| **Vercel** | Serverless | Hạn chế | ⭐⭐ Không khuyến nghị cho Flask |

---

## 🐍 1. PYTHONANYWHERE (KHUYẾN NGHỊ ⭐⭐⭐⭐⭐)

### ✅ Ưu điểm:
- Hoàn toàn miễn phí
- Dễ setup nhất
- Hỗ trợ Flask native
- SQLite hoạt động tốt
- Có web console
- Domain: `yourusername.pythonanywhere.com`

### 🚀 Bước 1: Đăng ký

1. Truy cập: https://www.pythonanywhere.com
2. Đăng ký tài khoản **Beginner (Free)**
3. Xác nhận email

### 🚀 Bước 2: Upload code

**Cách 1: Dùng Git (Khuyến nghị)**

```bash
# Trong PythonAnywhere Console
git clone https://github.com/Hikhai/ROOMMASTER.git
cd ROOMMASTER
```

**Cách 2: Upload trực tiếp**
- Dashboard → Files → Upload files
- Upload toàn bộ project (nén thành .zip trước)

### 🚀 Bước 3: Cài đặt dependencies

```bash
# Mở Bash Console trong PythonAnywhere
cd ~/ROOMMASTER

# Tạo virtual environment
mkvirtualenv --python=/usr/bin/python3.10 roommaster-env

# Kích hoạt virtualenv (tự động khi vào console sau này)
workon roommaster-env

# Cài đặt packages
pip install -r requirements.txt
```

### 🚀 Bước 4: Cấu hình .env

```bash
# Tạo file .env
cd ~/ROOMMASTER
nano .env

# Nội dung .env:
FLASK_ENV=production
SECRET_KEY=your-very-strong-secret-key-change-this
DATABASE_URL=sqlite:///roommaster.db
```

**Tạo SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 🚀 Bước 5: Khởi tạo database

```bash
workon roommaster-env
cd ~/ROOMMASTER

# Tối ưu database
python optimize_production.py

# Tạo dữ liệu mẫu (tùy chọn)
python seed_data.py
```

### 🚀 Bước 6: Cấu hình Web App

1. **Dashboard → Web → Add a new web app**
2. **Manual configuration** → Python 3.10
3. Điền thông tin:

**Source code:**
```
/home/yourusername/ROOMMASTER
```

**Working directory:**
```
/home/yourusername/ROOMMASTER
```

**Virtualenv:**
```
/home/yourusername/.virtualenvs/roommaster-env
```

**WSGI configuration file:** (Click để edit)
```python
import sys
import os

# Add project directory to path
project_home = '/home/yourusername/ROOMMASTER'  # ⚠️ Đổi yourusername
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Load .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from run import app as application
```

### 🚀 Bước 7: Cấu hình Static Files

Trong Web tab, thêm:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/ROOMMASTER/app/static/` |

### 🚀 Bước 8: Reload và test

1. Click **Reload** button màu xanh
2. Truy cập: `https://yourusername.pythonanywhere.com`
3. Đăng nhập: admin / admin123

### 🔧 Troubleshooting PythonAnywhere

**Lỗi 1: Import error**
```bash
# Kiểm tra virtualenv
workon roommaster-env
pip list  # Xem packages đã cài

# Cài lại nếu thiếu
pip install -r requirements.txt
```

**Lỗi 2: Database error**
```bash
cd ~/ROOMMASTER
workon roommaster-env
python optimize_production.py
```

**Lỗi 3: Static files không load**
- Kiểm tra path trong Static files mapping
- Đảm bảo có `/` ở cuối URL và Directory

**Xem logs:**
- Web tab → Log files → Error log
- Hoặc trong console: `tail -f /var/log/yourusername.pythonanywhere.com.error.log`

---

## 🚂 2. RENDER.COM (⭐⭐⭐⭐)

### ✅ Ưu điểm:
- Miễn phí với PostgreSQL
- Tự động deploy từ Git
- HTTPS miễn phí
- Custom domain miễn phí

### ⚠️ Giới hạn:
- Sleep sau 15 phút không dùng (khởi động lại mất ~30s)

### 🚀 Setup

1. **Push code lên GitHub** (nếu chưa có)

2. **Tạo file `render.yaml`:**
```yaml
services:
  - type: web
    name: roommaster
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: roommaster-db
          property: connectionString

databases:
  - name: roommaster-db
    databaseName: roommaster
    user: roommaster
```

3. **Thêm vào requirements.txt:**
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

4. **Deploy:**
   - Truy cập: https://render.com
   - Sign up với GitHub
   - New → Web Service
   - Connect repository: ROOMMASTER
   - Render tự động deploy

5. **Khởi tạo database:**
   - Shell tab → Open shell
   ```bash
   python optimize_production.py
   python seed_data.py
   ```

**URL:** `https://roommaster.onrender.com`

---

## 🚄 3. RAILWAY.APP (⭐⭐⭐⭐)

### ✅ Ưu điểm:
- Rất dễ deploy
- PostgreSQL miễn phí
- 500 giờ miễn phí/tháng
- Không sleep

### 🚀 Setup

1. **Tạo `Procfile`:**
```
web: gunicorn run:app
```

2. **Tạo `railway.json`:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

3. **Deploy:**
   - Truy cập: https://railway.app
   - Login với GitHub
   - New Project → Deploy from GitHub
   - Chọn repository ROOMMASTER
   - Add PostgreSQL database
   - Deploy

4. **Cấu hình variables:**
   - Settings → Variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-strong-key>
   DATABASE_URL=<auto-filled-from-postgres>
   ```

5. **Khởi tạo:**
   - Settings → Shell
   ```bash
   python optimize_production.py
   python seed_data.py
   ```

---

## ✈️ 4. FLY.IO (⭐⭐⭐)

### ✅ Ưu điểm:
- Persistent storage miễn phí
- Nhiều regions
- Docker-based

### 🚀 Setup

1. **Cài Fly CLI:**
```bash
# Windows (PowerShell)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

2. **Login:**
```bash
fly auth login
```

3. **Tạo `Dockerfile`:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python optimize_production.py

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
```

4. **Deploy:**
```bash
# Launch app
fly launch

# Tạo volume cho database
fly volumes create roommaster_data --size 1

# Deploy
fly deploy

# Khởi tạo database
fly ssh console
python seed_data.py
```

---

## 📊 SO SÁNH NHANH

### 🏆 PythonAnywhere - Tốt nhất cho người mới

**👍 Ưu điểm:**
- ✅ Setup dễ nhất (5 phút)
- ✅ Không cần Git
- ✅ SQLite hoạt động tốt
- ✅ Web console tiện lợi
- ✅ Không giới hạn uptime

**👎 Nhược điểm:**
- ❌ 512MB disk
- ❌ Không custom domain (free)
- ❌ CPU hạn chế

**Phù hợp:** Demo, học tập, dự án nhỏ

---

### 🥈 Render.com - Tốt cho production nhỏ

**👍 Ưu điểm:**
- ✅ PostgreSQL miễn phí
- ✅ HTTPS + Custom domain
- ✅ Auto deploy từ Git
- ✅ Logs tốt

**👎 Nhược điểm:**
- ❌ Sleep sau 15 phút
- ❌ Cold start ~30s

**Phù hợp:** Dự án cần PostgreSQL, không cần 24/7

---

### 🥉 Railway - Tốt cho development

**👍 Ưu điểm:**
- ✅ Không sleep
- ✅ PostgreSQL
- ✅ Dễ setup
- ✅ 500h/tháng

**👎 Nhược điểm:**
- ❌ Hết 500h thì stop
- ❌ Billing card required (không charge)

**Phù hợp:** Testing, staging environment

---

## 🎯 KHUYẾN NGHỊ THEO MỤC ĐÍCH

### 🎓 Nộp bài tập / Demo giảng viên
→ **PythonAnywhere**
- Dễ nhất, nhanh nhất
- Không cần Git
- Link ngay: `yourusername.pythonanywhere.com`

### 👨‍💼 Portfolio / CV
→ **Render.com**
- Professional
- Custom domain
- PostgreSQL (impressive)
- HTTPS

### 🧪 Testing / Development
→ **Railway**
- Không sleep
- Dễ iterate
- PostgreSQL

### 💼 Production thực tế
→ **VPS** (DigitalOcean, Vultr $5/tháng)
- Full control
- Better performance
- Xem DEPLOYMENT.md

---

## 🔥 QUICK START - PYTHONANYWHERE

### Checklist 5 phút:

1. **Đăng ký:** pythonanywhere.com
2. **Bash console:**
   ```bash
   git clone https://github.com/Hikhai/ROOMMASTER.git
   cd ROOMMASTER
   mkvirtualenv --python=/usr/bin/python3.10 roommaster-env
   pip install -r requirements.txt
   ```

3. **Tạo .env:**
   ```bash
   nano .env
   # Paste nội dung từ .env.example
   # Đổi SECRET_KEY
   ```

4. **Init database:**
   ```bash
   python optimize_production.py
   python seed_data.py
   ```

5. **Web App:**
   - Add new web app → Manual → Python 3.10
   - Source code: `/home/yourusername/ROOMMASTER`
   - Virtualenv: `/home/yourusername/.virtualenvs/roommaster-env`
   - Edit WSGI file (copy từ trên)
   - Static files: `/static/` → `/home/yourusername/ROOMMASTER/app/static/`
   - **Reload**

6. **Test:** `https://yourusername.pythonanywhere.com`

---

## 🆘 HỖ TRỢ

### PythonAnywhere
- Forum: https://www.pythonanywhere.com/forums/
- Help: https://help.pythonanywhere.com/

### Render
- Discord: https://discord.gg/render
- Docs: https://render.com/docs

### Railway
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app/

---

## 💡 TIPS

### 1. Tăng tốc PythonAnywhere
```python
# Trong config.py - ProductionConfig
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'connect_args': {'check_same_thread': False}
}
```

### 2. Monitor uptime (Render/Railway)
- Dùng UptimeRobot.com (miễn phí)
- Ping mỗi 5 phút để tránh sleep

### 3. Custom domain miễn phí
- Freenom.com (domain .tk, .ml, .ga)
- Cloudflare DNS (HTTPS miễn phí)

### 4. Backup database
```bash
# PythonAnywhere - Schedule với Task
# Dashboard → Tasks → Add new scheduled task
# Command: cd /home/yourusername/ROOMMASTER && python backup_db.py
```

---

## 🎉 HOÀN THÀNH!

**Deploy thành công? Chia sẻ link của bạn:**
- PythonAnywhere: `https://yourusername.pythonanywhere.com`
- Render: `https://roommaster.onrender.com`
- Railway: `https://roommaster-production.up.railway.app`

**Demo của mình:**
- URL: `https://hikhai.pythonanywhere.com/roommaster`
- Login: admin / admin123

**Chúc bạn deploy thành công! 🚀**
