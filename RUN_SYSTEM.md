# 🚀 RUN SYSTEM - Hướng Dẫn Chạy Hệ Thống

**Ngày Cập Nhật:** May 11, 2026  
**Trạng Thái:** Ready for Execution  
**Ngôn Ngữ:** Vietnamese / English

---

## 📋 QUICK START (5 Phút)

### Bước 1: Setup Backend

```bash
# Vào thư mục backend
cd backend

# Tạo virtual environment (nếu chưa có)
python -m venv venv

# Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# HOẶC
source venv/bin/activate       # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt

# Kiểm tra .env
cat .env  # Phải có GEMINI_API_KEY=AIzaSy...
```

### Bước 2: Khởi Động Backend

```bash
# Chắc chắn vẫn trong backend/
# Virtual environment đã activate

python app.py

# Nên thấy:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### Bước 3: Mở Frontend

```bash
# Từ thư mục dự án gốc:
# Tùy chọn A: Mở trực tiếp trong trình duyệt
start frontend/learning.html

# HOẶC Tùy chọn B: Dùng simple server
cd frontend
python -m http.server 8000
# Rồi mở: http://localhost:8000/learning.html
```

### Bước 4: Kiểm Thử

```
1. Mở http://localhost:8000/learning.html
2. Dán code mẫu (xem dưới)
3. Nhấp "Analyze"
4. Chọn bug type từ taxonomy
5. Nhấp "Get Hints"
6. Sửa code và test
7. Theo dõi progress
```

---

## 🔧 DETAILED SETUP

### Prerequisite 1: Python 3.12.6+

```bash
python --version
# Expected: Python 3.12.6 or higher

# Nếu không có, tải từ: https://www.python.org/
```

### Prerequisite 2: GCC (Windows MinGW-W64)

**STATUS:** ⏳ CRITICAL - Phải cài đặt

```bash
# Step 1: Kiểm tra xem GCC có không
gcc --version

# Step 2: Nếu không có, tải MinGW-W64
# URL: https://www.mingw-w64.org/downloads/
# Chọn: x86_64 architecture
# Cài vào: C:\Program Files\mingw-w64\

# Step 3: Thêm vào PATH
# Windows Settings → Environment Variables → PATH
# Thêm: C:\Program Files\mingw-w64\x86_64-...\bin

# Step 4: Kiểm tra lại
gcc --version
# Expected: gcc (GCC) X.X.X
```

### Prerequisite 3: API Key

```bash
# File: backend/.env
# Phải chứa:
GEMINI_API_KEY=AIzaSyCvCYqjq5V3i9thEGd73lpuhfwWMZVXTEM
FLASK_ENV=development
FLASK_DEBUG=True

# Kiểm tra:
cd backend
cat .env
```

---

## 📁 FILE STRUCTURE

```
backend/
├── app.py                    # Flask app chính
├── analyzer.py               # Compile & run C code
├── ai_handler.py            # Gemini API
├── hint_service.py          # Hint generation
├── learning_routes.py       # Interactive API routes
├── db_manager.py            # SQLite management
├── bug_taxonomy.py          # Bug classification
├── models.py                # Data models
├── prompt_generator.py      # Smart prompts
├── config.py                # Configuration
├── utils.py                 # Utilities
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── .gitignore
└── analyzer.db             # SQLite database (tự tạo)

frontend/
├── learning.html           # Interactive UI
├── learning.js             # Client logic
├── script.js              # Original analyzer JS
├── style.css              # Styling
└── index.html             # Original analyzer UI

c_samples/
├── sample1_loop_error.c
├── sample2_factorial.c
├── sample3_digit_count.c
├── sample4_max_value.c
└── sample5_reverse_number.c

documentation/
├── README.md
├── QUICK_START.md
├── INSTALL_GCC.md
├── TESTING_GUIDE.md        # ← Hướng dẫn test
└── ... (20+ file)
```

---

## 🎯 TEST CASES

### Sample 1: Loop Off-by-One Error

**File:** `c_samples/sample1_loop_error.c`

```c
#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int sum = 0;
    
    // BUG: Điều kiện sai (i < 5 thay vì i <= 5 nếu cần include 5)
    for (int i = 0; i < 5; i++) {
        sum += arr[i];
    }
    
    printf("Sum: %d\n", sum);
    return 0;
}
```

**Test Case:**
- Input: (không có)
- Expected Output: `Sum: 150`
- Bug Type: LOOP_ERROR (LP001)
- Fix: Loop condition đúng rồi, nhưng nếu khác yêu cầu...

### Sample 2: Conditional Logic Error

```c
#include <stdio.h>
int main() {
    int x = 5;
    
    // BUG: Điều kiện sai
    if (x < 5) {  // Should be x <= 5
        printf("Less than or equal to 5\n");
    } else {
        printf("Greater than 5\n");
    }
    
    return 0;
}
```

**Test Case:**
- Input: 5
- Expected: `Less than or equal to 5`
- Actual: `Greater than 5` ❌
- Fix: Change `x < 5` → `x <= 5`

### Sample 3: Off-by-One in Array

```c
#include <stdio.h>
int main() {
    int arr[] = {1, 2, 3, 4, 5};
    
    // BUG: Không include element cuối cùng
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    
    return 0;
}
```

---

## 🌐 API ENDPOINTS

### Health Check

```bash
curl http://localhost:5000/api/health
# Response: {"status": "ok"}
```

### Start Learning Session

```bash
curl -X POST http://localhost:5000/api/interactive/start-learning \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "problem_id": "cond_1",
    "code": "#include <stdio.h>\nint main() { if (5 < 5) printf(\"less\"); return 0; }",
    "requirements": "Print less when x <= 5",
    "testcases": [{"input": "", "expected_output": "less"}],
    "bug_type": "CONDITIONAL_LOGIC",
    "bug_taxonomy_id": "CF001"
  }'
```

**Response:**
```json
{
  "success": true,
  "attempt_id": 1,
  "analysis": {...},
  "initial_hints": [...]
}
```

### Get Next Hint

```bash
curl -X POST http://localhost:5000/api/interactive/get-hint \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 1,
    "hint_level": 1
  }'
```

### Modify Code and Test

```bash
curl -X POST http://localhost:5000/api/interactive/modify-code \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 1,
    "new_code": "#include <stdio.h>\nint main() { if (5 <= 5) printf(\"less\"); return 0; }",
    "testcases": [{"input": "", "expected_output": "less"}]
  }'
```

---

## 🖥️ RUNNING SERVERS (Multiple Terminals)

### Terminal 1: Backend

```bash
cd backend
.\venv\Scripts\Activate.ps1
python app.py
# Listening on: http://localhost:5000
```

### Terminal 2: Frontend (Optional)

```bash
cd frontend
python -m http.server 8000
# Listening on: http://localhost:8000
```

### Terminal 3: API Testing

```bash
# Test curl commands
curl http://localhost:5000/api/health
curl http://localhost:5000/api/interactive/get-bug-taxonomy
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Python 3.12.6+ installed
- [ ] GCC/MinGW-W64 installed and in PATH
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured with GEMINI_API_KEY
- [ ] Backend starts without errors
- [ ] Frontend loads learning.html
- [ ] Health check endpoint responds
- [ ] Can start learning session (attempt created)
- [ ] Can get hints from AI
- [ ] Can modify code and test
- [ ] Database records attempts correctly

---

## 🐛 TROUBLESHOOTING

### Error: "Module not found: analyzer"
```
Solution: cd backend first, make sure Python path is correct
python app.py
```

### Error: "GCC not found"
```
Solution: Install MinGW-W64, add to PATH, restart terminal
gcc --version
```

### Error: "GEMINI_API_KEY not set"
```
Solution: Check backend/.env file
cat .env
# Should have: GEMINI_API_KEY=...
```

### Error: "Port 5000 already in use"
```
Solution: Either:
1. Kill process using port 5000
   lsof -i :5000 && kill -9 <PID>
2. Use different port:
   export FLASK_PORT=5001 && python app.py
```

### Error: "Database locked"
```
Solution: Close other Python processes, delete analyzer.db
rm analyzer.db
python app.py  # Will recreate
```

---

## 📊 EXPECTED BEHAVIOR

### Successful Start

Backend:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Frontend:
- Page loads with code editor
- Can select bug taxonomy
- Can paste C code
- Can submit for analysis

### Full Workflow

1. **Submit code:**
   - User pastes C code
   - System analyzes for bugs
   - Display bug taxonomy matches

2. **Get hints:**
   - User clicks "Get Hints"
   - System calls AI
   - Displays 3 progressive hints

3. **Modify code:**
   - User edits code
   - Clicks "Run Tests"
   - System compiles & runs
   - Shows test results

4. **Track progress:**
   - Progress bar updates
   - Steps recorded in database
   - Can view history

---

## 🎓 LEARNING FLOW

```
User ──> Paste Code ──> Analyze
  ↓
Select Bug Type ──> Get Hints
  ↓
View Level 1 Hint ──> Modify Code
  ↓
Run Tests ──> All Pass? 
  ├─ YES ──> Celebrate! Record Success
  └─ NO ──> Get Level 2 Hint ──> Repeat
```

---

## 📈 MONITORING

### Check Backend Status
```bash
curl http://localhost:5000/api/health
# {"status": "ok"}
```

### View Database
```bash
cd backend
sqlite3 analyzer.db
sqlite> SELECT * FROM attempts;
sqlite> SELECT * FROM attempt_steps;
.exit
```

### View Logs
```bash
# Backend logs appear in terminal
# Frontend console: F12 → Console tab
```

---

## 🎁 SAMPLE WORKFLOW (Complete)

```bash
# 1. Terminal 1: Start backend
cd backend
.\venv\Scripts\Activate.ps1
python app.py

# 2. Terminal 2: Open frontend
start frontend/learning.html
# Or: cd frontend && python -m http.server 8000

# 3. In browser:
# - Input code
# - Select bug type
# - Click Analyze
# - Click Get Hints
# - Read hint, modify code
# - Click Run Test
# - Check results
# - Repeat or submit

# 4. Terminal 3: View results
sqlite3 backend/analyzer.db
> SELECT * FROM attempts WHERE id = 1;
> SELECT * FROM attempt_steps WHERE attempt_id = 1;
```

---

## 📞 SUPPORT

### Check Documentation

1. **For System Overview:** `IDEA_INTERACTIVE_LEARNING.md`
2. **For Testing:** `TESTING_GUIDE.md`
3. **For Setup:** `QUICK_START.md` / `INSTALL_GCC.md`
4. **For Development:** `DEVELOPER_GUIDE.md`

### Common Tasks

| Task | Solution |
|------|----------|
| Change GCC path | Edit analyzer.py line ~ |
| Change API key | Edit backend/.env |
| Change port | Set FLASK_PORT env var |
| Reset database | Delete analyzer.db |
| View database | `sqlite3 analyzer.db` |

---

## ⚡ PERFORMANCE TIPS

1. **Reduce AI latency:**
   - Cache hints if same bug detected
   - Use shorter prompts

2. **Database optimization:**
   - Add indexes for user_id, problem_id
   - Archive old attempts

3. **Frontend optimization:**
   - Use code editor with syntax highlighting
   - Cache taxonomy list

---

**Status:** 🟢 Ready to Run  
**Last Check:** May 11, 2026  
**Next:** Execute and test workflow

---

*For Issues: Check TROUBLESHOOTING section above*
