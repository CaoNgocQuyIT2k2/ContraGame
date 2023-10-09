import pygame, sys, os
from settings import *
from app.game_objects.shared.button import Button
from app.scenes import start_menu

class GameOver:
    def __init__(self):
        """Khởi tạo các biến của pygame"""
        self.done = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Âm thanh
        music_path = os.path.join(AUDIO_DIR, "leap.wav")
        self.music = pygame.mixer.Sound(music_path)
        self.music.play(loops=1)

    def get_font(self, size):
        font_path = os.path.join(GRAPHICS_DIR, "menu", "font.ttf")
        return pygame.font.Font(font_path, size)

    def display_game_over(self):
        while not self.done:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((249, 131, 103))

            # Hiển thị tiêu đề "GAME OVER"
            header_text = self.get_font(100).render("GAME OVER", True, "#d7fcd4")
            header_text_rect = header_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3))
            self.screen.blit(header_text, header_text_rect)

            # Tạo nút "REPLAY"
            replay_text = Button(
                image=None,
                pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.6),
                text_input="REPLAY",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="Red",
            )

            replay_text.changeColor(mouse_pos)
            replay_text.update(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_text.checkForInput(mouse_pos):
                        self.music.stop()
                        start_menu.StartMenu().main_menu()

        pygame.quit()
        sys.exit()
