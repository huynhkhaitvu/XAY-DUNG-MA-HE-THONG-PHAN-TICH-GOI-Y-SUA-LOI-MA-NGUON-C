# 🚀 HƯỚNG DẪN DEPLOYMENT

Hướng dẫn triển khai C Code Analyzer lên production.

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │ (Static HTML/CSS/JS)
│  (index.html)   │ ← Có thể host trên:
└────────┬────────┘    - Apache
         │             - Nginx
         │ HTTP        - GitHub Pages
         ↓
┌─────────────────┐
│   Backend API   │ (Flask)
│  (app.py)       │ ← Deploy trên:
└────────┬────────┘    - Heroku
         │             - Azure
         │             - AWS EC2
         ↓
┌─────────────────┐
│  GCC Compiler   │ (MinGW)
│                 │
└─────────────────┘
```

## 1️⃣ Production Setup Checklist

- [ ] Cài Python 3.12+ trên server
- [ ] Cài GCC (MinGW)
- [ ] Clone repository
- [ ] Setup virtual environment
- [ ] Cài Python packages
- [ ] Cấu hình Gemini API key
- [ ] Setup web server (Nginx/Apache)
- [ ] Configure firewall
- [ ] Setup SSL/TLS
- [ ] Setup monitoring/logging

## 2️⃣ Deployment Options

### Option A: Heroku (Dễ nhất)

#### Prerequisites
```powershell
# Install Heroku CLI
choco install heroku-cli
heroku login
```

#### Steps
1. Tạo `Procfile` trong backend:
```
web: gunicorn app:app
```

2. Cài Heroku buildpack cho GCC:
```bash
heroku buildpacks:add https://github.com/railwayapp/heroku-buildpack-gcc.git
```

3. Deploy:
```bash
git push heroku main
```

### Option B: Azure App Service

1. Tạo App Service trên Azure Portal
2. Connect GitHub repo
3. Azure tự động build & deploy
4. Cấu hình environment variables

### Option C: AWS EC2 (Flexible)

1. Tạo EC2 instance (Ubuntu/Windows Server)
2. SSH vào instance
3. Setup theo hướng dẫn Local

### Option D: Docker (Recommended)

Tạo `Dockerfile`:

```dockerfile
FROM python:3.12-slim

# Install GCC
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV FLASK_ENV=production
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build & Run:
```bash
docker build -t c-analyzer .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key c-analyzer
```

## 3️⃣ Backend Server Setup (Linux/Unix)

### Install dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3.12 gcc make
sudo apt-get install -y nginx
sudo apt-get install -y supervisor
```

### Setup app
```bash
cd /var/www/c-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Setup supervisor (auto-restart)
```ini
[program:c-analyzer]
directory=/var/www/c-analyzer
command=/var/www/c-analyzer/venv/bin/python app.py
autostart=true
autorestart=true
```

## 4️⃣ Frontend Deployment

### Option 1: Serve từ cùng server (Recommended)

Thêm vào Flask:
```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../frontend', filename)
```

### Option 2: GitHub Pages

1. Push `frontend` folder to GitHub
2. Enable GitHub Pages in repo settings
3. Update API_BASE_URL trong script.js:
```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

### Option 3: Separate Web Server

Setup Nginx:
```nginx
server {
    listen 80;
    server_name frontend.your-domain.com;
    
    root /var/www/c-analyzer/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 5️⃣ SSL/TLS Certificate

### Using Let's Encrypt (Free)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Update Nginx:
```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    # ... rest of config
}
```

## 6️⃣ Environment Variables

Production `.env`:
```
GEMINI_API_KEY=AIzaSyCvCYqjq5V3i9thEGd73lpuhfwWMZVXTEM
FLASK_ENV=production
FLASK_DEBUG=False
MAX_CODE_SIZE=50000
REQUEST_TIMEOUT=30
```

## 7️⃣ Monitoring & Logging

### Setup Logging
```python
import logging

logging.basicConfig(
    filename='/var/log/c-analyzer.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Use APM Tools
- Datadog
- New Relic
- Sentry (for error tracking)

## 8️⃣ Performance Tuning

### Backend
- Use Gunicorn with multiple workers:
```bash
gunicorn --workers 4 --threads 2 app:app
```

- Enable caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Frontend
- Minify CSS/JS
- Enable gzip compression in Nginx:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

## 9️⃣ Database (Optional)

Nếu cần lưu lịch sử:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c-analyzer.db'
db = SQLAlchemy(app)

class CodeAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    result = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

## 🔟 Health Checks

Setup endpoint cho monitoring:
```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'gcc': check_gcc(),
        'api': check_gemini_api()
    }
```

## 📊 Deployment Checklist

```
[ ] Environment variables configured
[ ] SSL certificate installed
[ ] Database migrated (if applicable)
[ ] Static files optimized
[ ] Logging configured
[ ] Monitoring setup
[ ] Backup strategy
[ ] Disaster recovery plan
[ ] Load testing completed
[ ] Security audit done
[ ] DNS configured
```

---

**Chúc mừng! Ứng dụng của bạn đã sẵn sàng production! 🎉**
