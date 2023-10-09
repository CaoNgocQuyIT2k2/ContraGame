import pygame, sys, os
from app.game_objects.shared.button import Button
from app.app import App
from settings import *

class StartMenu:
    def __init__(self):
        # Khởi tạo pygame và cửa sổ menu
        pygame.init()
        pygame.display.set_caption("Menu")
        background_path = os.path.join(GRAPHICS_DIR, "menu", "background.png")
        self.background = pygame.image.load(background_path)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Âm thanh
        music_path = os.path.join(AUDIO_DIR, "leap.wav")
        self.music = pygame.mixer.Sound(music_path)
        self.music.play(loops=1)

    def get_font(self, size):
        font_path = os.path.join(GRAPHICS_DIR, "menu", "font.ttf")
        return pygame.font.Font(font_path, size)

    def play(self):
        # Dừng âm thanh và chạy game
        self.music.stop()
        app = App()
        app.run()

    def options(self):
        while True:
            self.screen.fill((249, 131, 103))
            mouse_pos = pygame.mouse.get_pos()

            # Hiển thị tiêu đề màn hình Options
            screen_header = self.get_font(45).render("Game options", True, "#d7fcd4")
            screen_header_rect = screen_header.get_rect(center=(WINDOW_WIDTH / 2, 260))
            self.screen.blit(screen_header, screen_header_rect)

            # Tạo nút "BACK"
            go_back_text = Button(
                image=None,
                pos=(WINDOW_WIDTH / 2, 460),
                text_input="BACK",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="Red",
            )

            go_back_text.changeColor(mouse_pos)
            go_back_text.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back_text.checkForInput(mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:
            self.screen.fill((249, 131, 103))
            mouse_pos = pygame.mouse.get_pos()

            # Hiển thị tiêu đề màn hình Main Menu
            header_text = self.get_font(100).render("MAIN MENU", True, "#d7fcd4")
            header_text_rect = header_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.15))
            self.screen.blit(header_text, header_text_rect)

            # Tạo nút "PLAY"
            play_button_path = os.path.join(GRAPHICS_DIR, "menu", "play_rect.png")
            play_button = Button(
                image=pygame.image.load(play_button_path),
                pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.30),
                text_input="PLAY",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="White",
            )

            # Tạo nút "OPTIONS"
            options_button_path = os.path.join(GRAPHICS_DIR, "menu", "options_rect.png")
            options_button = Button(
                image=pygame.image.load(options_button_path),
                pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.45),
                text_input="OPTIONS",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="White",
            )

            # Tạo nút "QUIT"
            quit_button_path = os.path.join(GRAPHICS_DIR, "menu", "quit_rect.png")
            quit_button = Button(
                image=pygame.image.load(quit_button_path),
                pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.60),
                text_input="QUIT",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="White",
            )

            self.screen.blit(header_text, header_text_rect)

            for button in [play_button, options_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Hiển thị hướng dẫn sử dụng phím và bắn đạn
            instructions_text = self.get_font(30).render("Shoot: Space Bar", True, "#d7fcd4")
            instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.7))
            self.screen.blit(instructions_text, instructions_rect)

            instructions_text = self.get_font(30).render("Move: Arrow keys", True, "#d7fcd4")
            instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.75))
            self.screen.blit(instructions_text, instructions_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.play()
                    if options_button.checkForInput(mouse_pos):
                        self.options()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
