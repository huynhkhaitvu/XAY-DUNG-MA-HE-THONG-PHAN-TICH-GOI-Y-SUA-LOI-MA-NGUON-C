# 📑 C CODE ANALYZER - PROJECT INDEX

**Chào mừng!** 👋 Đây là hệ thống phân tích và gợi ý sửa lỗi mã C.

---

## 🚀 BẮT ĐẦU NGAY (3 bước)

### 1️⃣ Đọc file này: [QUICK_START.md](QUICK_START.md)
Hướng dẫn setup trong 5 phút - Đơn giản nhất!

### 2️⃣ Cài đặt GCC (nếu chưa có)
Xem: [INSTALL_GCC.md](INSTALL_GCC.md)

### 3️⃣ Chạy: `python backend/app.py`
Rồi mở `frontend/index.html`

---

## 📚 HƯỚNG DẪN THEO MỤC ĐÍCH

### 👤 Tôi là người dùng bình thường
1. [QUICK_START.md](QUICK_START.md) - Setup nhanh
2. [README_VI.md](README_VI.md) - Hướng dẫn sử dụng chi tiết
3. Bắt đầu phân tích code!

### 👨‍💻 Tôi là nhà phát triển
1. [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Cấu trúc code
2. [README_VI.md](README_VI.md) - API endpoints
3. Bắt đầu coding!

### 🚀 Tôi muốn deploy lên server
1. [DEPLOYMENT.md](DEPLOYMENT.md) - Các tùy chọn deployment
2. [README_VI.md](README_VI.md) - Configuration
3. Chọn platform và deploy!

### 🔧 Tôi cần cấu hình API
1. [SETUP_GEMINI_API.md](SETUP_GEMINI_API.md) - Tạo API key
2. Cập nhật file `.env` trong folder `backend`
3. Chạy lại backend

### ❓ Tôi gặp lỗi
1. Kiểm tra [README_VI.md](README_VI.md) - Troubleshooting
2. Chạy: `python backend/test_setup.py` - Diagnose
3. Xem logs console

---

## 📂 FILE STRUCTURE

```
📦 Project Root
│
├── 📖 DOCUMENTATION (Đọc những file này!)
│   ├── README_VI.md .................. ⭐ Bắt đầu ở đây
│   ├── QUICK_START.md ................ ⚡ 5 phút setup
│   ├── INSTALL_GCC.md ................ 🔧 Cài GCC
│   ├── SETUP_GEMINI_API.md ........... 🔑 API key
│   ├── DEPLOYMENT.md ................. 🚀 Deploy
│   ├── DEVELOPER_GUIDE.md ............ 👨‍💻 Code dev
│   ├── PROJECT_SUMMARY.md ............ 📊 Overview
│   └── INDEX.md (file này) ........... 🗂️ Navigation
│
├── ⚙️ BACKEND (Python Flask)
│   ├── app.py ....................... Flask app chính
│   ├── analyzer.py .................. Phân tích C
│   ├── ai_handler.py ................ Gemini AI
│   ├── config.py .................... Configuration
│   ├── utils.py ..................... Utility functions
│   ├── requirements.txt ............. Dependencies
│   ├── .env ......................... API key config
│   ├── .env.example ................. Template .env
│   ├── test_setup.py ................ Diagnostic tool
│   └── venv/ ........................ Virtual environment
│
├── 🎨 FRONTEND (HTML/CSS/JS)
│   ├── index.html ................... Giao diện chính
│   ├── style.css .................... Styling
│   └── script.js .................... Client logic
│
├── 🧪 SAMPLES (Ví dụ code C)
│   ├── sample1_loop_error.c ......... Loop bug example
│   ├── sample2_factorial.c .......... Factorial example
│   ├── sample3_digit_count.c ........ Digit count example
│   ├── sample4_max_value.c .......... Max value example
│   └── sample5_reverse_number.c .... Reverse number example
│
├── 🔐 KEYS
│   └── api_key/ ..................... Gemini API folder
│
├── .gitignore ....................... Git ignore rules
├── setup.ps1 ........................ PowerShell setup
└── INDEX.md (this file) ............. Navigation
```

---

## ✅ CHECKLIST - BẠN ĐÃ SẴN SÀNG?

Hãy kiểm tra các yêu cầu:

- [ ] Python 3.12+ đã cài (chạy: `python --version`)
- [ ] GCC đã cài (chạy: `gcc --version`)
- [ ] Có Gemini API key (hoặc có sẵn: `AIzaSyCvCYqjq5V3i9thEGd73lpuhfwWMZVXTEM`)
- [ ] Clone/download project này
- [ ] Đọc QUICK_START.md

**Nếu tất cả ✅ → Bắt đầu ngay!**

---

## 🎯 5 BƯỚC ĐẦU TIÊN

### Bước 1: Setup Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Bước 2: Kiểm tra Setup
```powershell
python test_setup.py
```
Nếu thấy ✅ xanh = OK!

### Bước 3: Chạy Backend
```powershell
python app.py
```
Nếu thấy `Running on http://127.0.0.1:5000` = OK!

### Bước 4: Mở Frontend
- Cách 1: Mở file `frontend/index.html` trực tiếp
- Cách 2: `cd frontend && python -m http.server 8000` → http://localhost:8000

### Bước 5: Test
1. Copy code C ở `c_samples/sample1_loop_error.c`
2. Paste vào editor
3. Nhấp "Phân tích"
4. Xem gợi ý từ AI 🤖

---

## 🆘 QUICK HELP

### Lỗi: "gcc: command not found"
→ Xem [INSTALL_GCC.md](INSTALL_GCC.md)

### Lỗi: "Connection refused"
→ Chạy `python backend/app.py` trước

### Lỗi: "API key invalid"
→ Xem [SETUP_GEMINI_API.md](SETUP_GEMINI_API.md)

### Lỗi: CORS error
→ Backend chưa chạy, hoặc port khác

### Cần help thêm?
→ Xem [README_VI.md](README_VI.md) phần Troubleshooting

---

## 🔗 QUICK LINKS

| Purpose | File |
|---------|------|
| 📖 Full Guide | [README_VI.md](README_VI.md) |
| ⚡ Quick Start | [QUICK_START.md](QUICK_START.md) |
| 🔧 GCC Setup | [INSTALL_GCC.md](INSTALL_GCC.md) |
| 🔑 API Setup | [SETUP_GEMINI_API.md](SETUP_GEMINI_API.md) |
| 🚀 Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) |
| 👨‍💻 Development | [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) |
| 📊 Project Info | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |

---

## 🌟 FEATURES HIGHLIGHT

✨ **Biên dịch C** - Sử dụng GCC  
✨ **Chạy chương trình** - Với input tùy chỉ  
✨ **Kiểm thử** - Auto-test với multiple testcases  
✨ **Phân tích** - Detect lỗi compile & logic  
✨ **AI Suggestions** - Gemini AI giúp sửa lỗi  
✨ **Web UI** - Giao diện modern & responsive  

---

## 📞 SUPPORT CHANNELS

1. **Kiểm tra Docs** - 90% vấn đề được giải quyết ở README
2. **Chạy Diagnostic** - `python backend/test_setup.py`
3. **Check Logs** - Xem console output của Flask
4. **Stack Overflow** - Nếu error về Python/Flask

---

## 📈 NEXT STEPS

✅ **Done:**
- Backend Flask setup
- Frontend interface
- AI integration
- C code compilation
- Full documentation

🔄 **Now:**
1. Chọn section phù hợp ở trên
2. Follow hướng dẫn
3. Start coding!

🚀 **Future:**
- Add more AI providers
- Database integration
- User authentication
- Code version control
- Collaborative editing

---

## 📝 NOTES

- API key đã được cấu hình sẵn
- GCC chưa cài (xem INSTALL_GCC.md)
- Tất cả files Python đều có type hints
- Frontend không cần build process
- CORS đã enable cho development

---

## 🎓 LEARNING PATH

```
Beginner:
  1. QUICK_START.md
  2. Test với sample code
  3. Explore AI features

Intermediate:
  1. DEVELOPER_GUIDE.md
  2. Add custom test cases
  3. Modify frontend UI

Advanced:
  1. DEPLOYMENT.md
  2. Deploy ke production
  3. Add database
  4. Custom AI providers
```

---

## ✨ TIPS & TRICKS

💡 **Tip 1:** Sử dụng sample code để test  
💡 **Tip 2:** Mỗi analysis tốn ~2 giây  
💡 **Tip 3:** AI suggestions rất helpful cho logic bugs  
💡 **Tip 4:** Có thể modify frontend style.css dễ dàng  
💡 **Tip 5:** Add test cases giúp verify kết quả  

---

## 🎉 YOU'RE ALL SET!

Bạn có mọi thứ cần thiết. Bây giờ:

1. **Pick a guide** từ mục trên
2. **Follow the steps**
3. **Start analyzing code!**

---

**Created with ❤️**  
**Questions? Check the docs!** 📖  
**Ready? Let's go! 🚀**

---

**Last Updated:** May 11, 2026  
**Status:** ✅ Production Ready
