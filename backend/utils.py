"""
Utility functions
"""
import re
import os


def extract_includes(code):
    """Trích xuất các thư viện include từ code"""
    pattern = r'#include\s+[<"]([^>"]+)[>"]'
    return re.findall(pattern, code)


def extract_functions(code):
    """Trích xuất tên các hàm từ code"""
    pattern = r'\b\w+\s+(\w+)\s*\('
    return re.findall(pattern, code)


def detect_common_errors(code):
    """Phát hiện các lỗi logic phổ biến"""
    errors = []
    
    # Kiểm tra vòng lặp
    if 'for' in code:
        # Kiểm tra i < n (có thể nên là <=)
        if re.search(r'for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+', code):
            errors.append("Vòng lặp dùng '<' - có thể nên dùng '<=' tùy theo logic")
    
    # Kiểm tra khởi tạo biến max/min
    if 'max' in code.lower() or 'min' in code.lower():
        if 'max = 0' in code or 'min = 0' in code:
            errors.append("Khởi tạo max/min bằng 0 - có thể sai nếu có số âm")
    
    # Kiểm tra chia cho 0
    if '/ 0' in code or '/ zero' in code.lower():
        errors.append("Chia cho 0 - sẽ gây lỗi runtime")
    
    # Kiểm tra quên dấu chấm phẩy
    if 'printf' in code and not code.count(';') >= code.count('printf'):
        errors.append("Có thể thiếu dấu chấm phẩy ở cuối dòng")
    
    return errors


def format_code(code):
    """Format code với indentation"""
    lines = code.split('\n')
    formatted = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Giảm indent trước '}'
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Add formatted line
        if stripped:
            formatted.append('    ' * indent_level + stripped)
        else:
            formatted.append('')
        
        # Tăng indent sau '{'
        if stripped.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted)


def validate_c_syntax(code):
    """Kiểm tra cú pháp C cơ bản"""
    issues = []
    
    # Kiểm tra main function
    if 'int main' not in code and 'void main' not in code:
        issues.append("Thiếu main() function")
    
    # Kiểm tra include stdio.h
    if 'printf' in code and '#include <stdio.h>' not in code:
        issues.append("Dùng printf nhưng thiếu #include <stdio.h>")
    
    # Kiểm tra brace balance
    if code.count('{') != code.count('}'):
        issues.append(f"Mismatch braces: {{ {code.count('{')} vs }} {code.count('}')}")
    
    # Kiểm tra return statement
    if 'int main' in code and 'return' not in code:
        issues.append("main() không có return statement")
    
    return issues


def get_file_size(path):
    """Lấy kích thước file"""
    try:
        return os.path.getsize(path)
    except:
        return 0


def safe_truncate(text, max_length=1000):
    """Cắt text an toàn"""
    if len(text) > max_length:
        return text[:max_length] + f"\n... [Truncated, {len(text)-max_length} chars more]"
    return text
