🚀 **STARTUP GUIDE - MỞ HỆ THỐNG NHANH NHẤT**
═══════════════════════════════════════════════

## 🎯 MỤC TIÊU
**Nhấn đúp 1 file → Hệ thống chạy (backend + frontend)**

---

## ⭐ **CÁCH ĐƠN GIẢN NHẤT**

### Lần đầu tiên (5 phút):
```
1. SETUP_API_KEY.bat  ← Setup Gemini API Key
2. INSTALL_DEPENDENCIES.bat ← Cài Python packages
3. RUN.bat ← Khởi động hệ thống
```

### Mỗi lần sử dụng (10 giây):
```
1. RUN.bat ← XONG!
```

---

## 📂 **CÁC FILES BATCH MỚI**

| File | Mục đích | Chạy bao lâu |
|------|---------|------------|
| **🔴 RUN.bat** | Khởi động hệ thống | 10 giây |
| **🟠 SETUP_API_KEY.bat** | Setup API (lần 1) | 2 phút |
| **🟡 INSTALL_DEPENDENCIES.bat** | Cài packages (lần 1) | 5 phút |
| 🟢 START_SYSTEM.bat | Backup của RUN.bat | 10 giây |

---

## 🔍 **CHI TIẾT TỪNG BƯỚC**

### **BƯỚC 1: Setup Gemini API (LẦN ĐẦU)**

1. **Nhấn đúp:** `SETUP_API_KEY.bat`
2. **Làm theo hướng dẫn:**
   - Vào: https://aistudio.google.com/app/apikey
   - Bấm "Create API key"
   - Copy key
   - Tạo file `backend\.env`
   - Paste: `GEMINI_API_KEY=your-key-here`

### **BƯỚC 2: Cài Dependencies (LẦN ĐẦU)**

1. **Nhấn đúp:** `INSTALL_DEPENDENCIES.bat`
2. **Chờ cài xong** (2-5 phút)
3. **Bấm Enter để thoát**

### **BƯỚC 3: Khởi Động Hệ Thống**

1. **Nhấn đúp:** `RUN.bat`
2. **Kết quả:**
   - ✅ Terminal backend mở (dòng: "Running on http://127.0.0.1:5000")
   - ✅ Browser mở frontend (index.html)
3. **GIỮ TERMINAL BACKEND MỞ**

---

## 📊 **FLOW CHƯƠNG TRÌNH**

```
RUN.bat
  ↓
Kiểm tra GCC (C Compiler)
  ↓ ✓
Kiểm tra Python
  ↓ ✓
Kiểm tra Gemini API Key (.env)
  ↓ ✓
Khởi động Backend (Flask)
  ↓ [Terminal riêng]
Chờ 4 giây backend khởi động
  ↓
Mở Frontend (index.html)
  ↓ [Browser]
✅ HỆ THỐNG SẴN SÀNG!
```

---

## 🌐 **GIAO DIỆN SAU KHI MỞ**

### **index.html (Mặc định)**
- Phân tích mã C
- Biên dịch (Compile)
- Chạy test cases
- Xem AI suggestions

### **learning.html (Learning Mode)**
- Interactive learning
- AI tự động phân loại lỗi
- Hints từng level (1, 2, 3)
- Sửa lỗi hướng dẫn

**Cách mở learning.html:**
- Từ index.html: Bấm link "Learning"
- Hoặc mở file: `frontend/learning.html`

---

## 🔧 **TROUBLESHOOT NHANH**

### ❌ "GCC not found"
```
→ Cài MinGW-w64 từ: https://www.mingw-w64.org/
→ Restart Windows
```

### ❌ "Python not found"
```
→ Cài Python từ: https://www.python.org/
→ Chọn "Add to PATH"
→ Restart Windows
```

### ❌ "Backend không khởi động"
```
→ Chạy: INSTALL_DEPENDENCIES.bat
→ Rồi chạy: RUN.bat lại
```

### ❌ "Frontend không kết nối backend"
```
→ Refresh browser: Ctrl+R
→ Hoặc: Ctrl+Shift+R (hard refresh)
→ Check terminal backend có chạy không
```

### ❌ "Port 5000 đã bị chiếm"
```
→ Đóng ứng dụng khác dùng port 5000
→ Hoặc restart Windows
```

---

## 💡 **TIPS & TRICKS**

### 🎯 Tạo Shortcut trên Desktop
```
1. Chuột phải → RUN.bat
2. "Create shortcut"
3. "Yes" (tạo shortcut)
4. Kéo shortcut vào Desktop
5. Mỗi lần: Double-click shortcut
```

### 🎯 Nếu lỗi liên tục
```
1. Xóa file: analyzer.db (nếu có)
2. Chạy: INSTALL_DEPENDENCIES.bat (cài lại)
3. Chạy: RUN.bat
```

### 🎯 Kiểm tra kết nối manual
```
Mở browser:
http://localhost:5000/api/health
→ Nếu thấy {"status": "ok"} = Backend OK ✓
```

---

## 📌 **IMPORTANT - ĐỪNG QUÊN!**

⚠️ **GIỮ TERMINAL BACKEND MỞ KHI SỬ DỤNG**
- Đó là cửa sổ cmd có dòng: "Running on http://127.0.0.1:5000"
- Đừng đóng nó!
- Để dừng: Đóng terminal

⚠️ **LẦN ĐẦU SẼ CHẬM**
- Lần 1: Cài packages (5 phút)
- Lần 2+: Nhanh (10 giây)

⚠️ **GEMINI API KEY**
- Miễn phí 60 requests/phút
- Đủ dùng cho học tập
- Free tier: https://ai.google.dev/

---

## 📚 **TÀI LIỆU LIÊN QUAN**

| File | Mô tả |
|------|-------|
| HOW_TO_RUN.txt | Hướng dẫn chi tiết (dạng text) |
| 00_START_HERE.md | Giới thiệu chung về dự án |
| DEVELOPER_GUIDE.md | Hướng dẫn cho developers |
| README.md | Tài liệu chính |

---

## ✨ **QUY TRÌNH TÓM TẮT**

### 🟦 SETUP (Lần 1):
```
SETUP_API_KEY.bat
      ↓
INSTALL_DEPENDENCIES.bat
      ↓
RUN.bat ✅
```

### 🟩 NORMAL (Mỗi lần):
```
RUN.bat ✅
```

---

## 🎮 **BẮT ĐẦU NGAY**

1. **Mở Windows Explorer** (Win+E)
2. **Vào folder project**
3. **Nhấn đúp:** `RUN.bat`
4. **Chờ hệ thống mở**
5. **Bắt đầu sử dụng!** 🎉

---

**Good luck! 🚀**
