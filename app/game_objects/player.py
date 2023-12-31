import os
import sys
import pygame
from settings import *
from pygame.math import Vector2 as vector
from app.game_objects.shared.entity import Entity
from app.scenes.game_over import GameOver

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAVITY = 15
SPEED = 400
JUMP_SPEED = 1400
HEALTH = 10

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, shoot, music):
        super().__init__(pos, path, groups, shoot)

        # collision
        self.collision_sprites = collision_sprites

        # vertical movement
        self.gravity = GRAVITY
        self.jump_speed = JUMP_SPEED
        self.on_floor = False  # chỉ có thể nhảy khi player đang đứng trên mặt đất
        self.moving_floor = None

        # health
        self.health = HEALTH
        # music
        self.music = music

        return

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split("_")[0] + "_idle"
        # jump
        if not self.direction.y == 0 and not self.on_floor:
            self.status = self.status.split("_")[0] + "_jump"

        # duck
        if self.on_floor and self.duck:
            self.status = self.status.split("_")[0] + "_duck"

        return

    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom

        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                # nếu player đang đi xuống
                if self.direction.y > 0:
                    self.on_floor = True
                # kiểm tra xem có tiếp xúc với nền đang di chuyển hay không
                if hasattr(sprite, "direction"):
                    self.moving_floor = sprite
        return

    def input(self):
        """Nhận đầu vào từ bàn phím của player và thay đổi vị trí của sprite"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed
        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

        if keys[pygame.K_SPACE] and self.can_shoot:
            entity = self
            direction = vector(1, 0) if self.status.split("_")[0] == "right" else vector(-1, 0)
            y_offset = vector(0, -16) if not self.duck else vector(0, 10)
            pos = (self.rect.center + direction * 60) + y_offset

            self.shoot(pos, direction, entity)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.shoot_sound.play()

        return

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    # xảy ra va chạm bên trái
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # xảy ra va chạm bên phải
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x

                else:
                    # va chạm phía dưới
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    # va chạm phía trên
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.on_floor and not self.direction.y == 0:
            self.on_floor = False

    def move(self, dt):
        if self.duck and self.on_floor:
            self.direction.x = 0
        # di chuyển theo phương ngang
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision("horizontal")
        # di chuyển theo phương dọc và trọng lực
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt
        # dán player vào mặt đất
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision("vertical")
        self.moving_floor = None

    def check_death(self):
        if self.health <= 0:
            # pygame.quit()
            # sys.exit()
            self.music.stop()
            game_over = GameOver()
            game_over.display_game_over()

    def update(self, dt):
        self.old_rect = self.rect.copy()  # lưu lại frame trước đó để phát hiện va chạm
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()

        self.animate(dt)
        self.blink()

        # bộ đếm thời gian
        self.shoot_timer()
        self.invul_timer()

        # kiểm tra chết
        self.check_death()
        return
