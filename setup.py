import sys
from cx_Freeze import setup, Executable
from settings import *

# Danh sách các tệp và thư mục cần bao gồm trong gói cài đặt của ứng dụng
include_files = [
    "main.py",          # Tệp chính của ứng dụng
    "settings.py",      # Tệp chứa cài đặt
    "README.md",        # Tệp README (tùy chọn)
    "./app",            # Thư mục app chứa mã nguồn ứng dụng
    "./assets",         # Thư mục chứa tài nguyên như hình ảnh, âm thanh, v.v.
]

# Tên tệp thực thi sau khi biên dịch
targetName = "contra"

# Tên tệp chương trình chính
name = "main.py"

# Mô tả của ứng dụng
description = "Contra clone"

# Cấu hình cho quá trình biên dịch với cx_Freeze
options = {"build_exe": {"include_files": include_files, "path": sys.path}}

# Xác định nền chạy cho các nền tảng khác nhau
base = "Win32GUI" if sys.platform.lower() == "win32" else None

# Định nghĩa tệp thực thi và thêm vào danh sách các tệp thực thi
executable = Executable(script="main.py", targetName=targetName, base=base)
executables = [executable]

# Thiết lập thông tin về gói cài đặt
setup(name=name, version="0.1", description=description, options=options, executables=executables)
