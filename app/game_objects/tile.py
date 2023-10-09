import pygame
from settings import *
from pygame.math import Vector2 as vector

# Tốc độ của MovingPlatform
PLATFORM_SPEED = 200

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z  # Layer ảnh chất lên nền của game

class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        z = LAYERS["Level"]  # Layer của tile dùng cho va chạm
        super().__init__(pos, surf, groups, z)
        self.old_rect = self.rect.copy()  # Lưu lại vị trí trước đó để kiểm tra va chạm

class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        # Di chuyển dựa trên số thực
        self.direction = vector(0, -1)  # Hướng di chuyển của nền di động (lên trên)
        self.speed = PLATFORM_SPEED  # Tốc độ di chuyển của nền di động
        self.pos = vector(self.rect.topleft)  # Vị trí của nền di động

    def update(self, dt):
        self.old_rect = self.rect.copy()  # Lưu lại vị trí trước đó để kiểm tra va chạm
        self.pos.y += self.direction.y * self.speed * dt  # Cập nhật vị trí dựa trên hướng và tốc độ
        x_pos = round(self.pos.x)
        y_pos = round(self.pos.y)
        self.rect.topleft = (x_pos, y_pos)  # Cập nhật vị trí của nền di động
