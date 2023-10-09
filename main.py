from settings import * #cài đặt và hằng số từ tệp settings.py vào chương trình
from app.scenes.start_menu import StartMenu


if __name__ == "__main__":
    start_menu = StartMenu()
    start_menu.main_menu()
