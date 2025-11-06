# 🚀 Hướng dẫn đưa RoomMaster lên GitHub

## ✅ Đã hoàn thành

- [x] Khởi tạo git repository
- [x] Add tất cả files
- [x] Commit đầu tiên (72 files, 12605 lines)

## 📝 Các bước tiếp theo

### Bước 1: Tạo repository trên GitHub

1. Truy cập: https://github.com/new
2. Điền thông tin:
   - **Repository name**: `RoomMaster` (hoặc tên khác)
   - **Description**: `🏢 Hệ thống quản lý phòng trọ chuyên nghiệp - Flask web application`
   - **Visibility**: 
     - ✅ **Public** - Nếu muốn chia sẻ
     - ⬜ **Private** - Nếu muốn giữ riêng tư
   - **KHÔNG** chọn "Add README" (đã có sẵn)
   - **KHÔNG** chọn "Add .gitignore" (đã có sẵn)
   - **KHÔNG** chọn "Choose a license" (thêm sau nếu cần)

3. Click **"Create repository"**

### Bước 2: Kết nối repository local với GitHub

Sau khi tạo xong, GitHub sẽ hiện hướng dẫn. Chạy các lệnh sau trong terminal:

```powershell
# Thêm remote origin (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/RoomMaster.git

# Đổi branch thành main (GitHub dùng main thay vì master)
git branch -M main

# Push lên GitHub lần đầu
git push -u origin main
```

**LƯU Ý**: Thay `YOUR_USERNAME` bằng username GitHub của bạn!

### Bước 3: Nhập credentials

GitHub sẽ yêu cầu xác thực:

#### Option 1: GitHub Personal Access Token (Khuyến nghị)
1. Tạo token tại: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Chọn scopes: `repo` (full control of private repositories)
4. Click **"Generate token"**
5. **COPY TOKEN** (chỉ hiện 1 lần!)
6. Khi push, dùng token làm password

#### Option 2: GitHub CLI
```powershell
# Cài đặt GitHub CLI
winget install --id GitHub.cli

# Login
gh auth login

# Push
git push -u origin main
```

#### Option 3: SSH Key
```powershell
# Tạo SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Thêm vào GitHub: https://github.com/settings/keys
# Sau đó dùng SSH URL thay vì HTTPS
git remote set-url origin git@github.com:YOUR_USERNAME/RoomMaster.git
```

---

## 🔧 Commands nhanh

### Kiểm tra git status
```powershell
git status
git log --oneline
```

### Xem remote
```powershell
git remote -v
```

### Push lên GitHub
```powershell
git push origin main
```

### Thêm thay đổi mới
```powershell
git add .
git commit -m "Your commit message"
git push
```

---

## 📋 Checklist sau khi push

- [ ] Repository đã public/private đúng mong muốn
- [ ] README.md hiển thị đẹp trên GitHub
- [ ] Add topics: `flask`, `python`, `bootstrap`, `sqlite`, `room-management`
- [ ] Add description và website (nếu có)
- [ ] Tạo release tag v2.0.0
- [ ] (Optional) Add LICENSE file
- [ ] (Optional) Setup GitHub Pages cho documentation
- [ ] (Optional) Enable GitHub Actions cho CI/CD

---

## 🎨 Tùy chỉnh GitHub Repository

### 1. Add Topics
Repository → About → Settings → Topics:
```
flask, python, sqlalchemy, bootstrap, sqlite, room-management, 
rental-management, invoice-system, vietnamese, web-application
```

### 2. Add Description
```
🏢 Hệ thống quản lý phòng trọ chuyên nghiệp với Flask - Professional room rental management system
```

### 3. Create Release Tag
```powershell
git tag -a v2.0.0 -m "Release v2.0.0 - Production Ready"
git push origin v2.0.0
```

Sau đó vào GitHub:
- Releases → Create a new release
- Choose tag: v2.0.0
- Title: `v2.0.0 - Production Ready 🚀`
- Description: Copy từ CHANGELOG.md

### 4. Add LICENSE (Optional)

**MIT License** (khuyến nghị cho open source):

```powershell
# Tạo LICENSE file
@"
MIT License

Copyright (c) 2025 RoomMaster Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@ | Out-File -FilePath LICENSE -Encoding UTF8

git add LICENSE
git commit -m "Add MIT License"
git push
```

---

## 🔒 Security Best Practices

### Kiểm tra .gitignore
Đảm bảo các file sau KHÔNG được push:
- ✅ `.env` - Environment variables
- ✅ `instance/*.db` - Database files
- ✅ `logs/*.log` - Log files
- ✅ `__pycache__/` - Python cache
- ✅ `.venv/` - Virtual environment

### Verify trước khi push
```powershell
# Xem files sẽ được push
git ls-files

# Kiểm tra không có sensitive data
git log --all --full-history -- "**/.*env*"
```

---

## 🌟 Sau khi push thành công

### Repository URL
```
https://github.com/YOUR_USERNAME/RoomMaster
```

### Clone để test
```powershell
# Clone repository về máy khác
git clone https://github.com/YOUR_USERNAME/RoomMaster.git
cd RoomMaster

# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Run
python run.py
```

### Share với người khác
1. **URL**: `https://github.com/YOUR_USERNAME/RoomMaster`
2. **Documentation**: README.md tự động hiển thị
3. **Live demo**: Deploy lên Heroku/Railway/Render

---

## 🚀 Deploy Options

### Option 1: Heroku
```powershell
# Install Heroku CLI
winget install Heroku.HerokuCLI

# Login
heroku login

# Create app
heroku create roommaster-app

# Set env vars
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Open
heroku open
```

### Option 2: Railway.app
1. Visit: https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose RoomMaster
5. Add environment variables
6. Deploy!

### Option 3: Render.com
1. Visit: https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
5. Add environment variables
6. Deploy!

---

## 📞 Troubleshooting

### Error: "failed to push"
```powershell
# Pull trước khi push
git pull origin main --rebase
git push origin main
```

### Error: "remote origin already exists"
```powershell
# Xóa remote cũ
git remote remove origin

# Thêm lại
git remote add origin https://github.com/YOUR_USERNAME/RoomMaster.git
```

### Error: "Authentication failed"
- Dùng Personal Access Token thay vì password
- Hoặc setup SSH key
- Hoặc dùng GitHub CLI

---

## ✅ Quick Commands Summary

```powershell
# 1. Kiểm tra status
git status

# 2. Add remote (CHỈ LẦN ĐẦU)
git remote add origin https://github.com/YOUR_USERNAME/RoomMaster.git

# 3. Đổi branch name
git branch -M main

# 4. Push lên GitHub
git push -u origin main

# 5. Verify
git remote -v
```

---

**🎉 Chúc mừng! Dự án của bạn đã sẵn sàng trên GitHub!**

Share link với bạn bè: `https://github.com/YOUR_USERNAME/RoomMaster`
