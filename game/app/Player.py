from Character import Char
import pygame

class Player(Char):
    
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
        self.level = 1
        self.xp = 0
        self.xp_required = 50
        self.kills = 0
        self.max_hp = hp
        self.hp_display = hp
        self.hp_actual = hp
        self.invincible = False
        self.invincible_time = 2000  # длительность неуязвимости в миллисекундах
        self.last_hit_time = 0
        self.regen = 0
        self.regen_cooldown = 1000
        self.last_regen = 0
    
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
        
        if self.invincible:
            # визуальный эффект — игрок мигает
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                temp_image = self.image.copy()
                temp_image.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(temp_image, self.rect)
                return
        
        return super().draw(screen)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    def get_speed(self):
        return super().get_speed()
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6 and self.rect.y <=554:
                self.rect.x -= self.speed - 1
                self.rect.y += self.speed - 1
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6 and self.rect.y >= 6:
                self.rect.x -= self.speed - 1
                self.rect.y -= self.speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764 and self.rect.y <= 554:
                self.rect.x += self.speed - 1
                self.rect.y += self.speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764 and self.rect.y >= 6:
                self.rect.x += self.speed - 1
                self.rect.y -= self.speed - 1
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764:
                self.rect.x += self.speed
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if self.rect.y >= 6:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if self.rect.y <= 554:
                self.rect.y += self.speed
        