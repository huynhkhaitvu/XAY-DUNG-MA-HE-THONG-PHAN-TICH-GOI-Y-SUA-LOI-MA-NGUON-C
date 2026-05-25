# 🚀 QUICK START GUIDE

Hướng dẫn nhanh để bắt đầu sử dụng C Code Analyzer.

## ⚡ 5 Phút Setup (Windows)

### 1️⃣ Kiểm Tra Yêu Cầu Cơ Bản

```powershell
python --version      # Phải là 3.12+
gcc --version        # Phải có GCC
```

**Nếu thiếu:**
- Python: Tải từ https://www.python.org/
- GCC: Xem file `INSTALL_GCC.md`

### 2️⃣ Cấu Hình Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

✅ Xong! API key đã được cấu hình sẵn

### 3️⃣ Chạy Backend

```powershell
python app.py
```

Bạn sẽ thấy:
```
 * Running on http://127.0.0.1:5000
```

### 4️⃣ Mở Frontend

Mở file `frontend/index.html` trong trình duyệt

### 5️⃣ Bắt Đầu Sử Dụng

1. Dán mã C vào editor
2. Thêm test case (tuỳ chọn)
3. Nhấp "Phân tích" để kiểm tra

---

## 🧪 Test Setup

Nếu muốn kiểm tra toàn bộ setup:

```powershell
cd backend
python test_setup.py
```

Sẽ kiểm tra:
- ✅ Python version
- ✅ GCC installation
- ✅ Flask dependencies
- ✅ .env configuration
- ✅ C compilation

---

## 📝 Ví Dụ Đầu Tiên

Dán code này vào editor:

```c
#include <stdio.h>
int main() {
    int sum = 0;
    for (int i = 1; i < 5; i++) {  // BUG: < thay vì <=
        sum += i;
    }
    printf("Sum: %d\n", sum);
    return 0;
}
```

Thêm test case:
- **Input:** (trống)
- **Expected Output:** Sum: 10

Nhấp "Phân tích" → AI sẽ gợi ý lỗi! 🎯

---

## 🔧 Cấu Hình API Key (Nếu Cần)

API key đã được cấu hình. Nếu cần thay đổi:

1. Mở `backend/.env`
2. Tạo API key mới: https://aistudio.google.com/app/apikey
3. Thay thế `GEMINI_API_KEY=...`
4. Lưu file

---

## 🛑 Gặp Lỗi?

| Lỗi | Giải Pháp |
|-----|----------|
| `gcc: command not found` | Cài MinGW-w64 (xem INSTALL_GCC.md) |
| Connection refused | Chạy `python app.py` |
| CORS error | Reload trang, backend phải chạy |
| AI không response | Kiểm tra API key, quota hết |

---

## 📚 Thêm Tài Liệu

- **README_VI.md** - Hướng dẫn chi tiết
- **INSTALL_GCC.md** - Cài GCC chi tiết
- **SETUP_GEMINI_API.md** - Cài API key chi tiết

---

## ⏱️ Troubleshooting Nhanh

```powershell
# Kiểm tra GCC
gcc --version

# Kiểm tra Python modules
python -c "import flask; print('OK')"

# Kiểm tra API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10])"

# Kiểm tra biên dịch mã C
# Tạo file test.c với code C bất kỳ
gcc test.c -o test.exe
.\test.exe
```

---

**Bây giờ bạn đã sẵn sàng! Enjoy! 🎉**
