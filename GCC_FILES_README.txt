🔧 GCC INSTALLATION FILES - CHỈ DẪN SỬ DỤNG
═════════════════════════════════════════════════════════════

📌 TÌNH HUỐNG: Máy không có GCC

═════════════════════════════════════════════════════════════
🎯 NHANH NHẤT (Chỉ 3 bước)
─────────────────────────────

1️⃣ Chạy file này:
   AUTO_INSTALL_GCC.bat
   (Chuột phải → Run as administrator)

2️⃣ Chờ cài xong (3-5 phút)

3️⃣ Restart PowerShell
   → Test: gcc --version
   → Rồi chạy: RUN.bat

═════════════════════════════════════════════════════════════
📋 CÁC FILES BATCH
─────────────────────

| File | Mục đích | Khi nào dùng |
|------|---------|------------|
| **AUTO_INSTALL_GCC.bat** | Cài GCC tự động | Lần 1 (Chính) |
| CHECK_GCC.bat | Kiểm tra GCC | Trước/Sau khi cài |
| ADD_GCC_TO_PATH.bat | Thêm vào PATH | Nếu cài rồi chưa có PATH |
| INSTALL_WITH_CHOCOLATEY.bat | Cài bằng Chocolatey | Alternative |

═════════════════════════════════════════════════════════════
📖 CÁC FILES HƯỚNG DẪN
─────────────────────

| File | Nội dung |
|------|---------|
| **NO_GCC_FIX.txt** | Giải pháp nhanh (đọc trước) |
| **GCC_SETUP.txt** | Hướng dẫn toàn diện |
| **INSTALL_GCC_GUIDE.txt** | 3 cách cài chi tiết |

═════════════════════════════════════════════════════════════
🔍 KIỂM TRA GCC
──────────────

Trước/sau khi cài, chạy:
  CHECK_GCC.bat

Hoặc trong PowerShell:
  gcc --version

═════════════════════════════════════════════════════════════
✅ QUY TRÌNH HOÀN CHỈNH
──────────────────────

KIỂM TRA:
  Nhấn đúp: CHECK_GCC.bat
  • ✓ Thấy version → Bỏ qua
  • ❌ "not found" → Đến CÀI

CÀI ĐẶT:
  Nhấn đúp: AUTO_INSTALL_GCC.bat
  (Chuột phải → Run as administrator)

KIỂM TRA LẠI:
  Nhấn đúp: CHECK_GCC.bat
  • ✓ Thấy version → OK!

THÊM VÀO PATH (nếu cần):
  Nhấn đúp: ADD_GCC_TO_PATH.bat

CHẠY HỆ THỐNG:
  Nhấn đúp: RUN.bat

═════════════════════════════════════════════════════════════
⚠️ QUAN TRỌNG
──────────────

• Batch files cần "Run as Administrator"
• Sau khi cài → RESTART PowerShell
• Hoặc restart Windows để PATH cập nhật

═════════════════════════════════════════════════════════════
🆘 TROUBLESHOOT
───────────────

GCC vẫn "not found" sau khi cài?
  1. Restart PowerShell (đừng chỉ restart terminal)
  2. Hoặc restart Windows
  3. Chạy: ADD_GCC_TO_PATH.bat
  4. Test: gcc --version

AUTO_INSTALL_GCC.bat lỗi?
  1. Đảm bảo chạy "Run as Administrator"
  2. Hoặc cài Chocolatey trước
  3. Hoặc dùng: INSTALL_WITH_CHOCOLATEY.bat

═════════════════════════════════════════════════════════════

BƯỚC 1: Đọc NO_GCC_FIX.txt
BƯỚC 2: Chạy AUTO_INSTALL_GCC.bat
BƯỚC 3: Restart PowerShell
BƯỚC 4: Chạy RUN.bat

═════════════════════════════════════════════════════════════
