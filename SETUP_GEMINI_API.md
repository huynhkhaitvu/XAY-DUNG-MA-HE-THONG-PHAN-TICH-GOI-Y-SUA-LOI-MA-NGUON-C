# HƯỚNG DẪN SETUP API KEY GEMINI

## Bước 1: Truy cập Google AI Studio

1. Mở trình duyệt, truy cập: https://aistudio.google.com/app/apikey
2. Nếu chưa đăng nhập, đăng nhập bằng Google Account
3. Đọc và chấp nhận điều khoản

## Bước 2: Tạo API Key

1. Chọn **"Create API key"** hoặc **"+ Create new secret key"**
2. Chọn **"Create API key in new project"**
3. Copy API key được tạo

## Bước 3: Cấu Hình Ứng Dụng

### Cách 1: Dùng File .env (Khuyến Nghị)

1. Mở folder `backend`
2. Copy file `.env.example` thành `.env`
3. Mở `.env` bằng editor (VS Code, Notepad, v.v.)
4. Thay `your_api_key_here` bằng API key:
```
GEMINI_API_KEY=sk-...your_api_key_here...
```
5. Lưu file

### Cách 2: Dùng File api_key_gemini.txt

1. Mở file `api_key/api_key_gemini.txt`
2. Dán API key vào
3. Lưu file

## Bước 4: Kiểm Tra API Key

Chạy backend:
```bash
cd backend
python app.py
```

Nếu không có lỗi, API key đã được cấu hình đúng ✅

## ⚠️ Lưu Ý An Toàn

1. **KHÔNG** commit `.env` file lên Git
2. **KHÔNG** share API key công khai
3. Kiểm tra quota sử dụng tại: https://aistudio.google.com/app/apikey
4. Nếu API key bị lộ, xóa ngay và tạo cái mới

## Giới Hạn API

- Gemini API có giới hạn yêu cầu miễn phí
- Nếu vượt quá, cần nâng cấp thành tài khoản trả phí
- Kiểm tra sử dụng: https://console.cloud.google.com/

## Gặp Vấn Đề?

### "Invalid API Key"
- Kiểm tra copy đầy đủ API key
- Kiểm tra không có khoảng trắng thừa

### "Quota Exceeded"
- Đã dùng hết quota miễn phí
- Nâng cấp tài khoản hoặc tạo project mới

### "401 Unauthorized"
- API key sai
- Project không có quyền
- Tạo API key mới

---

**Sau khi cấu hình xong, quay lại README.md để chạy ứng dụng.**
