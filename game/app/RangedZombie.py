import pygame
import math
import random
from Character import Char

class EnemyBullet:
    """Простая пуля врага"""
    def __init__(self, x, y, target_pos, speed=5, damage=2):
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 50, 50))  # красная пуля
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = damage

        # направление полета (в сторону игрока)
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.vel_x = dx / dist * speed
        self.vel_y = dy / dist * speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class RangedZombie(Char):
    """Враг, стреляющий в игрока"""
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
        self.attack_cooldown = 5000  # 3 секунды между выстрелами
        self.last_attack_time = 0
        self.shoot_distance = 300  # дистанция, с которой начинает стрелять
        self.max_hp = hp
        self.hp_actual = hp
        self.hp_display = hp
        self.random_offset_x = random.uniform(-0.2, 0.2)
        self.random_offset_y = random.uniform(-0.2, 0.2)


    def move_and_attack(self, player_rect, player_center, bullets_list, others):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        # вектор к игроку
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < 0.01:
            dist = 0.01
        dx /= dist
        dy /= dist

        # рандомное смещение
        if not hasattr(self, "random_offset_x"):
            import random
            self.random_offset_x = random.uniform(-0.5, 0.5)
            self.random_offset_y = random.uniform(-0.5, 0.5)

        move_x = dx * self.speed + self.random_offset_x
        move_y = dy * self.speed + self.random_offset_y

        # отталкивание от других врагов
        avoid_x, avoid_y = 0, 0
        for other in others:
            if other is self:
                continue
            dist_x = self.rect.centerx - other.rect.centerx
            dist_y = self.rect.centery - other.rect.centery
            dist_o = math.hypot(dist_x, dist_y)
            if 0 < dist_o < 40:
                avoid_x += dist_x / dist_o
                avoid_y += dist_y / dist_o

        # нормализуем вектор отталкивания
        avoid_dist = math.hypot(avoid_x, avoid_y)
        if avoid_dist > 0:
            avoid_x /= avoid_dist
            avoid_y /= avoid_dist

        # добавляем отталкивание
        move_x += avoid_x * 0.5
        move_y += avoid_y * 0.5

        # движение
        if dist > self.shoot_distance + 50:
            self.rect.x += move_x
            self.rect.y += move_y
        elif dist < self.shoot_distance - 40:
            self.rect.x -= dx * self.speed / 1.5
            self.rect.y -= dy * self.speed / 1.5
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.last_attack_time = current_time
                bullet = EnemyBullet(self.rect.centerx, self.rect.centery, player_rect.center, damage=2)
                bullets_list.append(bullet)

        # ограничение по экрану
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)



    def draw(self, screen):
        if self.hp_display > self.hp_actual:
            self.hp_display -= 0.5  # скорость "анимации ухода HP"
        if self.hp_display < self.hp_actual:
            self.hp_display = self.hp_actual

        # Полоска параметров
        bar_width = 40
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.y - 12  # над головой

        # Проценты HP
        ratio_actual = max(self.hp_actual / self.max_hp, 0)
        ratio_display = max(self.hp_display / self.max_hp, 0)

        # --- Рисуем полоску ---

        # Чёрная рамка
        pygame.draw.rect(screen, (0, 0, 0), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))

        # Красный фон (потерянное HP)
        pygame.draw.rect(screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Жёлтая "анимация урона" — выбывающая полоска
        pygame.draw.rect(screen, (255, 200, 50), (bar_x, bar_y, bar_width * ratio_display, bar_height))
        
        # Зелёная актуальная HP-полоска (мгновенная)
        pygame.draw.rect(screen, (0, 220, 70), (bar_x, bar_y, bar_width * ratio_actual, bar_height))
        
        screen.blit(self.image, self.rect)
