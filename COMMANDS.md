# ⚡ COMMANDS REFERENCE

Quick reference cho các commands thường dùng.

---

## 🚀 STARTUP COMMANDS

### Setup Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Run Backend
```powershell
python app.py
# Output: Running on http://127.0.0.1:5000
```

### Run Frontend (Option 1: Direct)
```
Mở file: frontend/index.html
```

### Run Frontend (Option 2: HTTP Server)
```powershell
cd frontend
python -m http.server 8000
# Truy cập: http://localhost:8000
```

### Test Setup
```powershell
python test_setup.py
# Sẽ check: Python, GCC, Flask, .env, C compilation
```

---

## 🔍 DIAGNOSTIC COMMANDS

### Check Python Version
```powershell
python --version     # Phải 3.12+
python -c "import sys; print(sys.version)"
```

### Check GCC Installation
```powershell
gcc --version        # Phải có GCC
gcc -print-file-name=cc1
```

### Check Python Modules
```powershell
python -c "import flask; print('Flask OK')"
python -c "import requests; print('Requests OK')"
python -c "import dotenv; print('dotenv OK')"
```

### Check Gemini API Key
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10])"
```

### Check Backend Connection
```powershell
curl http://localhost:5000/api/health
# Hoặc từ PowerShell:
Invoke-WebRequest -Uri "http://localhost:5000/api/health"
```

### Check GCC Compilation
```powershell
# Tạo file test.c
# gcc test.c -o test.exe
# .\test.exe
```

---

## 📝 DEVELOPMENT COMMANDS

### Install Dependencies
```powershell
pip install -r requirements.txt

# Install dev tools
pip install pytest pytest-cov black flake8

# Upgrade pip
python -m pip install --upgrade pip
```

### Code Formatting
```powershell
black *.py                    # Format code
black --check *.py           # Check formatting

flake8 *.py                  # Lint code
```

### Run Tests
```powershell
pytest                       # Run all tests
pytest -v                    # Verbose
pytest -s                    # Show print output
pytest --cov=.              # Coverage report
pytest test_setup.py -v      # Run specific test
```

### Generate API Documentation
```powershell
# Using Sphinx (if installed)
sphinx-build -b html docs/ docs/_build/
```

---

## 🔧 CONFIGURATION COMMANDS

### Create .env File
```powershell
# From .env.example
Copy-Item backend\.env.example backend\.env

# Edit file
code backend\.env  # In VS Code
# Or edit manually
```

### Verify .env
```powershell
# Check if .env exists and has API key
if (Test-Path backend\.env) { 
    Get-Content backend\.env 
}
```

### Change FLASK_ENV
```powershell
# Windows PowerShell
$env:FLASK_ENV = "development"    # development/production/testing

# Check current
echo $env:FLASK_ENV
```

---

## 🐛 DEBUGGING COMMANDS

### Verbose Flask Output
```python
# In app.py or run:
app.run(debug=True)  # Show detailed errors
```

### Python Debugging
```python
# Add to code:
import pdb
pdb.set_trace()  # Breakpoint

# Commands:
# c - continue
# n - next line
# s - step into
# p var - print variable
# l - list code
# q - quit
```

### Check Process Port
```powershell
# Check what's on port 5000
netstat -ano | findstr :5000

# Kill process on port 5000
taskkill /PID <PID> /F
```

### View Logs
```powershell
# Flask logs appear in console
# To save to file:
python app.py > logs.txt 2>&1
```

---

## 📦 PACKAGE MANAGEMENT

### Update Requirements
```powershell
pip freeze > requirements.txt
```

### Install From Requirements
```powershell
pip install -r requirements.txt
```

### Uninstall Package
```powershell
pip uninstall flask
```

### List Installed Packages
```powershell
pip list
pip show flask  # Details of specific package
```

---

## 🧹 CLEANUP COMMANDS

### Remove Virtual Environment
```powershell
Remove-Item venv -Recurse -Force
```

### Remove Python Cache
```powershell
Remove-Item __pycache__ -Recurse -Force
Remove-Item *.pyc
```

### Remove Compiled Files
```powershell
Remove-Item *.exe
Remove-Item *.o
```

### Clean All Temp Files
```powershell
# Windows
for /r %i in (__pycache__) do @echo %i
del /s __pycache__
del /s *.pyc

# PowerShell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item
```

---

## 🔐 SECURITY COMMANDS

### Check API Key Exposure
```powershell
# Search for API key in files (should not be found)
grep -r "AIzaSy" .

# Or in PowerShell:
Select-String -Path "*.py" -Pattern "AIzaSy"
```

### Verify .gitignore
```powershell
# Check if .env is ignored
git check-ignore .env

# Check if api_key files are ignored
git check-ignore api_key/*
```

---

## 🚀 DEPLOYMENT COMMANDS

### Using Gunicorn
```powershell
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t c-analyzer .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key c-analyzer
```

### Using Heroku
```bash
heroku login
heroku create
git push heroku main
```

---

## 📊 PERFORMANCE COMMANDS

### Monitor System Resources
```powershell
Get-Process python | Select-Object Name, CPU, Memory
```

### Profile Python Code
```python
# Add to code:
import cProfile
cProfile.run('analyze_code(...)')
```

### Time Execution
```python
import time
start = time.time()
# ... code ...
print(f"Took {time.time() - start}s")
```

---

## 🔄 GIT COMMANDS

### Initialize Git (if not done)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <url>
git push -u origin main
```

### Ignore API Keys
```bash
echo ".env" >> .gitignore
echo "api_key/" >> .gitignore
git add .gitignore
git commit -m "Add .gitignore"
```

### Check What Would Be Committed
```bash
git status
git diff
```

---

## 📞 HELP COMMANDS

### Get Python Help
```powershell
python -h              # Python help
python -c help(flask) # Module help
```

### Flask Help
```powershell
# From Python:
python
>>> import flask
>>> help(flask)
```

### GCC Help
```powershell
gcc --help
gcc -v --help         # Verbose help
```

### Curl/HTTP Help
```powershell
curl --help
curl -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d '{"code":"..."}'
```

---

## 💡 USEFUL ONE-LINERS

### Test if backend is alive
```powershell
while ($true) { try { Invoke-WebRequest http://localhost:5000/api/health -EA Ignore | % StatusCode } catch { Write-Host "..." }; sleep 1 }
```

### Kill all Python processes
```powershell
Get-Process python | Stop-Process -Force
```

### Find all .py files
```powershell
Get-ChildItem -Recurse -Filter *.py
```

### Count lines of code
```powershell
(Get-ChildItem -Recurse -Filter *.py | Get-Content | Measure-Object -Line).Lines
```

### Show recent files
```powershell
Get-ChildItem -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

---

## 🎯 TROUBLESHOOTING FLOWCHART

```
Problem: Backend won't start
├─ python app.py
├─ python test_setup.py
└─ Check .env file exists

Problem: GCC not found
├─ gcc --version
├─ Check PATH environment variable
└─ Reinstall MinGW-w64

Problem: Connection refused
├─ Ensure backend is running
├─ Check port 5000 is available
└─ netstat -ano | findstr :5000

Problem: API key invalid
├─ Check .env has correct key
├─ Create new API key
└─ Test with: python -c "..."

Problem: Code compilation fails
├─ Check C code syntax
├─ Test with: gcc test.c -o test.exe
└─ Check compiler output
```

---

## 📚 REFERENCE RESOURCES

- Python: https://docs.python.org/3/
- Flask: https://flask.palletsprojects.com/
- GCC: https://gcc.gnu.org/
- Gemini API: https://ai.google.dev/
- Bootstrap: https://getbootstrap.com/docs/5.3/

---

**Last Updated:** May 11, 2026  
**Status:** ✅ Complete

---

*Save this file for quick reference!* 📌
