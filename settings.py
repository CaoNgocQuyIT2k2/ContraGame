import os

# Kích thước cửa sổ trò chơi
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Độ ưu tiên của các lớp trong bản đồ TMX
LAYERS = {
    "BG": 0,                  # Lớp nền
    "BG Detail": 1,           # Chi tiết nền
    "Level": 2,               # Lớp mức chơi (có va chạm)
    "FG Detail Bottom": 3,    # Chi tiết phía trước dưới
    "FG Detail Top": 4        # Chi tiết phía trước trên
}

# Đường dẫn tới thư mục cơ sở (base directory) của ứng dụng
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn tới các thư mục chứa tài nguyên của trò chơi
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
DATA_DIR = os.path.join(ASSETS_DIR, "data")
GRAPHICS_DIR = os.path.join(ASSETS_DIR, "graphics")
