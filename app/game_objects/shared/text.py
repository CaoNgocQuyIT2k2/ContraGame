import pygame
from pygame.locals import *


class Text:
    """Lớp Text dùng để tạo đối tượng văn bản."""

    def __init__(self, text, pos, **options):
        # Lấy bề mặt hiển thị của pygame
        self.display_surface = pygame.display.get_surface()

        self.text = text  # Nội dung văn bản
        self.pos = pos    # Vị trí của văn bản

        self.fontname = None  # Tên font chữ
        self.fontsize = 72    # Kích thước font chữ mặc định
        self.fontcolor = Color("white")  # Màu chữ mặc định
        self.set_font()   # Thiết lập font chữ
        self.render()     # Render văn bản
        return

    def set_font(self):
        """Thiết lập font chữ từ tên và kích thước."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        return

    def render(self):
        """Tạo hình ảnh văn bản."""
        self.image = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        return

    def draw(self):
        """Vẽ hình ảnh văn bản lên màn hình."""
        self.display_surface.blit(self.image, self.rect)
        return
