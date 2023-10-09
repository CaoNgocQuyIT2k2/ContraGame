import pygame
import sys
import os
from settings import *
from pytmx.util_pygame import load_pygame
from app.game_objects.tile import Tile, CollisionTile, MovingPlatform
from app.game_objects.player import Player
from app.game_objects.all_sprites import AllSprites
from app.game_objects.bullet import Bullet, FireAnimation
from app.game_objects.enemy import Enemy
from app.game_objects.overlay import Overlay
from app.game_objects.shared.text import Text
from app.scenes.game_over import GameOver

class App:
    def __init__(self):
        """Khởi tạo các biến và cài đặt pygame."""
        self.running = True
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Contra")
        self.clock = pygame.time.Clock()

        # Âm thanh
        music_file_path = os.path.join(AUDIO_DIR, "music.wav")
        self.music = pygame.mixer.Sound(music_file_path)
        self.music.play(loops=1)

        # Nhóm các sprite
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

        # Hình ảnh đạn
        bullet_file_path = os.path.join(GRAPHICS_DIR, "bullet.png")
        fire_0_file_path = os.path.join(GRAPHICS_DIR, "fire", "0.png")
        fire_1_file_path = os.path.join(GRAPHICS_DIR, "fire", "1.png")
        self.bullet_surf = pygame.image.load(bullet_file_path).convert_alpha()
        fire_surf_1 = pygame.image.load(fire_0_file_path).convert_alpha()
        fire_surf_2 = pygame.image.load(fire_1_file_path).convert_alpha()
        self.fire_surfs = [fire_surf_1, fire_surf_2]

    def load_map_layer(self, layer_name, tile_type):
        """Nạp dữ liệu từ các lớp của bản đồ TMX vào trò chơi."""
        for x, y, surf in self.tmx_map.get_layer_by_name(layer_name).tiles():
            pos = (x * 64, y * 64)
            if tile_type == "standard":
                groups = self.all_sprites
                z = LAYERS[layer_name]
                Tile(pos, surf, groups, z)
            elif tile_type == "collision":
                groups = [self.all_sprites, self.collision_sprites]
                CollisionTile(pos, surf, groups)

    def load_moving_platforms(self):
        """Nạp dữ liệu về các nền di động vào trò chơi."""
        self.platform_border_rects = []

        for obj in self.tmx_map.get_layer_by_name("Platforms"):
            if obj.name == "Platform":
                pos = (obj.x, obj.y)
                surf = obj.image
                groups = [self.all_sprites, self.collision_sprites, self.platform_sprites]
                MovingPlatform(pos, surf, groups)
            else:  # Khung biên
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        """Xử lý va chạm giữa người chơi và các nền di động."""
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    # Nếu nền đang đi lên
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom  # Đổi vị trí hình chữ nhật
                        platform.pos.y = platform.rect.y  # Đổi vị trí tile
                        platform.direction.y = 1  # Đổi hướng di chuyển của nền
                    # Nếu nền đang đi xuống
                    else:
                        platform.rect.bottom = border.top  # Đổi vị trí hình chữ nhật
                        platform.pos.y = platform.rect.y  # Đổi vị trí tile
                        platform.direction.y = -1  # Đổi hướng di chuyển của nền
            # Kiểm tra xem người chơi có va chạm phía dưới nền di động không
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        """Xử lý va chạm của đạn với các vật cản và đối tượng có thể bị tấn công."""
        # Vật cản
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)

        # Đối tượng có thể bị tấn công
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage()

    def shoot(self, pos, direction, entity):
        """Tạo đạn và thêm nó vào nhóm các sprite đạn."""
        surf = self.bullet_surf
        groups = [self.all_sprites, self.bullet_sprites]
        Bullet(pos, surf, direction, groups)
        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

    def load_player_and_enemies(self):
        """Nạp người chơi và kẻ địch từ bản đồ TMX."""
        for obj in self.tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                pos = (obj.x, obj.y)
                shoot = self.shoot
                groups = [self.all_sprites, self.vulnerable_sprites]
                collision_sprites = self.collision_sprites
                path = os.path.join(GRAPHICS_DIR, "player")
                self.player = Player(pos, groups, path, collision_sprites, shoot, self.music)
            if obj.name == "Enemy":
                pos = (obj.x, obj.y)
                shoot = self.shoot
                groups = [self.all_sprites, self.vulnerable_sprites]
                collision_sprites = self.collision_sprites
                path = os.path.join(GRAPHICS_DIR, "enemies", "standard")
                player = self.player
                Enemy(pos, path, groups, shoot, player, collision_sprites)

    def setup(self):
        """Thiết lập trò chơi, bao gồm nạp bản đồ TMX và các đối tượng."""
        tmx_map_path = os.path.join(DATA_DIR, "map.tmx")
        self.tmx_map = load_pygame(tmx_map_path)

        # Hiển thị gạch đá và các đối tượng
        self.load_map_layer("Level", "collision")  # Hiển thị level riêng cho cơ chế va chạm
        layers = ["BG", "BG Detail", "FG Detail Bottom", "FG Detail Top"]
        for layer in layers:
            self.load_map_layer(layer, "standard")

        # Hiển thị người chơi và vị trí kẻ địch dưới dạng tile
        self.load_player_and_enemies()

        # Hiển thị nền di động có cơ chế va chạm
        self.load_moving_platforms()

    def unload(self):
        """Khi kết thúc trò chơi, hiển thị màn hình kết thúc."""
        self.display_surface.fill((249, 131, 103))
        self.music.stop()
        game_over = GameOver()
        game_over.display_game_over()

    def run(self):
        """Chạy vòng lặp chính của trò chơi."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.unload()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()
            self.all_sprites.custom_draw(self.player)
            self.overlay.display()

            pygame.display.update()

        pygame.quit()
        sys.exit()
