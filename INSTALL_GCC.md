# HƯỚNG DẪN CÀI ĐẶT MINGW-W64 TRÊN WINDOWS

## Bước 1: Tải MinGW-w64

Truy cập: https://www.mingw-w64.org/

Kéo xuống và click vào link tải: **mingw-w64-online-installer** hoặc tải trực tiếp:
https://sourceforge.net/projects/mingw-w64/files/

## Bước 2: Chạy Installer

1. Chạy file `mingw-w64-install.exe`
2. Chọn Settings:
   - Version: Mới nhất (8.1.0 hoặc cao hơn)
   - Architecture: x86_64
   - Threads: posix
   - Exception: seh
   - Build revision: Mới nhất

3. Chọn Destination folder: **C:\mingw64** (khuyến nghị)

4. Nhấp "Next" để cài đặt

## Bước 3: Thêm vào PATH

### Cách 1: Thêm thủ công (Windows 10/11)

1. Bấm **Windows + X**, chọn **System**
2. Chọn **Advanced system settings**
3. Chọn **Environment Variables**
4. Dưới "User variables" hoặc "System variables", chọn **Path**
5. Nhấp **Edit**
6. Nhấp **New** và thêm: `C:\mingw64\bin`
7. **OK** → **OK**

### Cách 2: Sử dụng PowerShell (Admin)

```powershell
$env:Path += ";C:\mingw64\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
```

Rồi **khởi động lại Terminal/PowerShell**

## Bước 4: Kiểm Tra Cài Đặt

Mở PowerShell mới và chạy:

```powershell
gcc --version
```

Nếu thấy version thông tin, cài đặt thành công! ✅

## Gặp Vấn Đề?

### GCC vẫn không tìm thấy
1. Kiểm tra `C:\mingw64\bin` tồn tại
2. Khởi động lại computer
3. Dùng full path: `C:\mingw64\bin\gcc.exe --version`

### Thử MSYS2 thay thế

Nếu MinGW không hoạt động, cài MSYS2:

```powershell
choco install msys2
```

Rồi mở MSYS2 và chạy:
```bash
pacman -S mingw-w64-x86_64-gcc
```

## Test Biên Dịch

Tạo file `test.c`:
```c
#include <stdio.h>
int main() {
    printf("Hello from GCC!\n");
    return 0;
}
```

Biên dịch:
```powershell
gcc test.c -o test.exe
.\test.exe
```

Nếu thấy "Hello from GCC!" - OK! ✅

---

**Sau khi GCC sẵn sàng, quay lại README.md để tiếp tục cài đặt ứng dụng.**
