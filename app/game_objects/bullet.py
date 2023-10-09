import pygame
from settings import *
from pygame.math import Vector2 as vector

BULLET_SPEED = 1200
MAX_LIFETIME = 1000


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)
        self.image = surf

        # Đảo hình ảnh nếu direction.x là số âm
        if direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["Level"]

        # Di chuyển dựa trên số thập phân
        self.direction = direction
        self.speed = BULLET_SPEED
        self.pos = vector(self.rect.center)

        # Hủy đạn sau một thời gian
        self.start_time = pygame.time.get_ticks()

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Hủy đạn sau một thời gian
        if (pygame.time.get_ticks() - self.start_time) > MAX_LIFETIME:
            self.kill()


class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)
        # Thiết lập
        self.entity = entity
        self.frames = surf_list
        self.z = LAYERS["Level"]

        # Đảo hướng của các khung hình cháy
        if direction.x < 0:
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

        # Hình ảnh
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Độ lệch để di chuyển hoạt hình cháy đến cuối nòng súng
        x_offset = 60 if direction.x > 0 else -60
        y_offset = 10 if entity.duck else -16
        self.offset = vector(x_offset, y_offset)

        # Vị trí
        self.rect = self.image.get_rect(center=self.entity.rect.center + self.offset)
        return

    def animate(self, dt):
        # Hủy sprite sau khi hoạt hình hoàn thành
        self.frame_index += 15 * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        # Hoạt hình sprite bằng cách sử dụng các khung hình
        else:
            self.image = self.frames[(int(self.frame_index))]
        return

    def move(self):
        self.rect.center = self.entity.rect.center + self.offset

    def update(self, dt):
        self.animate(dt)
        self.move()
