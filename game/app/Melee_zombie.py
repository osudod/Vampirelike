from Character import Char
import pygame
import random

class Melee(Char):
    
    def __init__(self, image, damage, hp, speed, x, y):
        self.image = pygame.image.load(image).convert_alpha()
        self.damage = damage
        self.hp = hp
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.random_offset_x = random.uniform(-0.2, 0.2)
        self.random_offset_y = random.uniform(-0.2, 0.2)
        # self.random_offset_x = 0
        # self.random_offset_y = 0
        self.max_hp = hp
        self.hp_actual = hp
        self.hp_display = hp
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

    
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
        
        return super().draw(screen)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    
    def move(self, target_rect, others):
        
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        
        # --- 1. Притягиваемся к игроку ---
        dx = target_rect.x - self.rect.x
        dy = target_rect.y - self.rect.y

        # нормализация для плавного движения
        length = (dx * dx + dy * dy) ** 0.5
        if length != 0:
            dx /= length
            dy /= length

        # применяем движение к игроку + лёгкий рандом (хаос)
        move_x = dx * self.speed + self.random_offset_x
        move_y = dy * self.speed + self.random_offset_y

        # --- 2. Отталкивание от других монстров поблизости ---
        avoid_x = 0
        avoid_y = 0
        for other in others:
            if other is self:
                continue
            dist_x = self.rect.x - other.rect.x
            dist_y = self.rect.y - other.rect.y
            dist = (dist_x * dist_x + dist_y * dist_y) ** 0.5

            # если другой монстр слишком близко — оттолкнуться
            if dist < 20 and dist > 0:  # радиус "толпы"
                avoid_x += dist_x / dist  # направление ОТ монстра
                avoid_y += dist_y / dist

        # прибавляем эффект расхождения монстров
        move_x += avoid_x * 0.2
        move_y += avoid_y * 0.2
        self.pos_x += move_x
        self.pos_y += move_y
        # print(move_x, move_y)
        # --- 3. Итоговое движение ---
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        
        # ограничение по экрану
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = self.rect.x  # не дать накопиться float-смещению
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.pos_x = self.rect.x

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos_y = self.rect.y
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.pos_y = self.rect.y
