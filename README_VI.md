# 🔧 Hệ Thống Phân Tích & Gợi Ý Sửa Lỗi Mã C

Ứng dụng web hỗ trợ phân tích lỗi logic trong mã C, biên dịch, chạy kiểm thử, và gợi ý sửa lỗi bằng AI (Gemini API).

## 📋 Tính Năng Chính

✅ **Biên dịch mã C** - Sử dụng GCC/MinGW-w64  
✅ **Chạy chương trình** - Với input tùy chỉnh  
✅ **Kiểm thử tự động** - So sánh output với testcase  
✅ **Phân tích lỗi** - Phát hiện lỗi biên dịch và logic  
✅ **Gợi ý AI** - Tích hợp Gemini API để gợi ý sửa  
✅ **Giao diện thân thiện** - Bootstrap 5 + modern UI  

## 🛠️ Stack Công Nghệ

### Backend
- **Python 3.12+**
- **Flask 2.3+** - Web framework
- **Requests** - Gọi Gemini API
- **Python-dotenv** - Quản lý biến môi trường
- **Flask-CORS** - Hỗ trợ CORS

### Frontend
- **HTML5**
- **Bootstrap 5** - Responsive CSS framework
- **Vanilla JavaScript** - Không cần framework
- **Highlight.js** - Syntax highlighting

### Biên Dịch & Thực Thi
- **GCC** (MinGW-w64 trên Windows)
- **Python subprocess** - Gọi GCC

### AI Integration
- **Gemini API** (Google)

## 📦 Cài Đặt

### 1. Yêu Cầu Hệ Thống
- Windows 10/11
- Python 3.12+
- Git (tuỳ chọn)

### 2. Cài GCC (MinGW-w64)

**Cách 1: Sử dụng Chocolatey (nếu có)**
```powershell
choco install mingw
```

**Cách 2: Tải trực tiếp**
1. Truy cập: https://www.mingw-w64.org/
2. Tải MinGW-w64 installer
3. Chạy installer
4. Chọn path: `C:\mingw64`
5. Hoàn tất cài đặt

**Cách 3: Sử dụng MSYS2**
```powershell
choco install msys2
```
Rồi trong MSYS2:
```bash
pacman -S mingw-w64-x86_64-gcc
```

**Kiểm tra cài đặt:**
```powershell
gcc --version
```

### 3. Cài Đặt Python Dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Cấu Hình Gemini API

1. Lấy API key từ: https://aistudio.google.com/apikey
2. Copy file `.env.example` thành `.env`
3. Dán API key vào:
```
GEMINI_API_KEY=your_api_key_here
```

## 🚀 Chạy Ứng Dụng

### Terminal 1: Backend
```bash
cd backend
venv\Scripts\activate
python app.py
```
Server sẽ chạy tại: `http://127.0.0.1:5000`

### Terminal 2: Frontend
Mở file `frontend/index.html` trong trình duyệt hoặc:
```bash
cd frontend
python -m http.server 8000
```
Truy cập: `http://localhost:8000`

## 📝 Cách Sử Dụng

### 1. Nhập Mã C
- Dán mã C vào editor bên trái
- Hoặc chọn từ thư mục `c_samples/`

### 2. Tạo Test Cases
- Nhấp "Thêm Test Case"
- Nhập Input và Expected Output
- Có thể thêm nhiều test cases

### 3. Phân Tích
- Nhấp "Phân tích" để:
  - Biên dịch mã
  - Chạy tất cả test cases
  - Nhận gợi ý từ AI nếu có lỗi

### 4. Xem Kết Quả
- Kết quả compile status
- Kết quả từng test case
- Gợi ý từ AI (nếu có lỗi)

## 📂 Cấu Trúc Thư Mục

```
XAY-DUNG-MA-HE-THONG-PHAN-TICH-GOI-Y-SUA-LOI-MA-NGUON-C/
│
├── backend/
│   ├── app.py                 # Flask app chính
│   ├── analyzer.py            # Module phân tích C
│   ├── ai_handler.py          # Module gọi Gemini API
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Template biến môi trường
│   └── venv/                  # Virtual environment
│
├── frontend/
│   ├── index.html             # Giao diện chính
│   ├── style.css              # Styling
│   └── script.js              # Logic JavaScript
│
├── c_samples/
│   ├── sample1_loop_error.c
│   ├── sample2_factorial.c
│   ├── sample3_digit_count.c
│   ├── sample4_max_value.c
│   └── sample5_reverse_number.c
│
├── api_key/
│   └── api_key_gemini.txt     # API key Gemini
│
└── README.md                  # File này
```

## 🔌 API Endpoints

### GET /api/health
Kiểm tra trạng thái server
```
Response: {"status": "ok", "message": "Server is running"}
```

### POST /api/compile
Biên dịch mã C
```json
{
  "code": "..."
}
```

### POST /api/run
Chạy mã C
```json
{
  "code": "...",
  "input": "..."
}
```

### POST /api/analyze
Phân tích toàn diện
```json
{
  "code": "...",
  "testcases": [
    {"input": "...", "expected_output": "..."}
  ]
}
```

### POST /api/suggestions
Lấy gợi ý từ AI
```json
{
  "code": "...",
  "error_message": "...",
  "output": "..."
}
```

## 🐛 Xử Lý Lỗi Thường Gặp

### GCC not found
**Nguyên nhân:** GCC chưa cài hoặc không trong PATH  
**Giải pháp:**
1. Cài MinGW-w64 (xem phần Cài Đặt)
2. Thêm `C:\mingw64\bin` vào PATH

### Connection refused
**Nguyên nhân:** Backend không chạy  
**Giải pháp:**
```bash
python app.py
```

### CORS error
**Nguyên nhân:** Frontend và Backend không cùng origin  
**Giải pháp:** Mặc định đã enable CORS, nếu lỗi kiểm tra app.py

### Gemini API error
**Nguyên nhân:** API key sai hoặc hết quota  
**Giải pháp:**
1. Kiểm tra `.env` file
2. Tạo API key mới từ https://aistudio.google.com/apikey
3. Kiểm tra quota API

## 🔐 Bảo Mật

⚠️ **Lưu ý quan trọng:**
- Không commit `.env` file chứa API key lên Git
- API key chỉ nên được cấu hình cục bộ
- Trong production, dùng environment variables hoặc secrets manager

## 📚 Ví Dụ Test Cases

### Ví dụ 1: Tính Tổng
```c
#include <stdio.h>
int main() {
    int n = 5;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    printf("%d", sum);
    return 0;
}
```
- Input: (không có)
- Expected Output: 15

### Ví dụ 2: Kiểm Tra Số Chẵn
```c
#include <stdio.h>
int main() {
    int n;
    scanf("%d", &n);
    if (n % 2 == 0) {
        printf("Chẵn");
    } else {
        printf("Lẻ");
    }
    return 0;
}
```
- Input: 4
- Expected Output: Chẵn

## 🤝 Đóng Góp

Nếu bạn tìm thấy bug hoặc có gợi ý, vui lòng:
1. Mở Issue
2. Gửi Pull Request
3. Liên hệ qua email

## 📞 Hỗ Trợ

Nếu cần hỗ trợ:
- Kiểm tra [Troubleshooting](#xử-lý-lỗi-thường-gặp)
- Đọc lại [Cài Đặt](#cài-đặt)
- Kiểm tra logs từ Backend

## 📄 Giấy Phép

MIT License - Tự do sử dụng và chỉnh sửa

## 📅 Changelog

### v1.0.0 (2026-05-11)
- ✅ Biên dịch và chạy mã C
- ✅ Phân tích lỗi
- ✅ Tích hợp Gemini AI
- ✅ Giao diện web hoàn chỉnh

---

**Phát triển bởi:** GitHub Copilot  
**Cập nhật lần cuối:** May 11, 2026
