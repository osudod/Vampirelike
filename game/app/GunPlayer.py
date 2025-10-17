import pygame
from Player import Player
from Bullet import Bullet

class GunPlayer(Player):
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
        self.attack_cooldown = 1500  # 1.5 сек
        self.last_attack_time = pygame.time.get_ticks()

        # Flash эффект
        self.flash_rect = None
        self.flash_time = 100  # 0.1 сек
        self.flash_created = 0

    def attack(self, monsters, bullets):
        if not monsters:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_cooldown:
            return

        # Поиск ближайшего монстра
        nearest = min(monsters, key=lambda m: ((m.rect.x - self.rect.x)**2 + (m.rect.y - self.rect.y)**2))

        # Создаем пулю
        bullet_speed = self.speed + 3
        # print(self.rect.center[0], self.rect.center[1])
        # print(f"mon - {nearest.rect.centerx, nearest.rect.centery}")
        bullets.append(Bullet(self.rect.centerx, self.rect.centery, nearest.rect.centerx, nearest.rect.centery, bullet_speed, self.damage))

        # Создаем flash эффект
        self.create_flash_effect(nearest)

        self.last_attack_time = pygame.time.get_ticks()

    def create_flash_effect(self, target):
        self.flash_rect = pygame.Rect(0, 0, 20, 20)

        # Определяем сторону цели
        if target.rect.centerx > self.rect.centerx:
            self.flash_rect.center = (self.rect.centerx + 30, self.rect.centery)
        elif target.rect.centerx < self.rect.centerx:
            self.flash_rect.center = (self.rect.centerx - 30, self.rect.centery)
        elif target.rect.centery < self.rect.centery:
            self.flash_rect.center = (self.rect.centerx, self.rect.centery - 30)
        else:
            self.flash_rect.center = (self.rect.centerx, self.rect.centery + 30)

        self.flash_created = pygame.time.get_ticks()

    def draw_flash(self, screen):
        if self.flash_rect:
            if pygame.time.get_ticks() - self.flash_created > self.flash_time:
                self.flash_rect = None
            else:
                s = pygame.Surface((self.flash_rect.width, self.flash_rect.height))
                s.set_alpha(160)
                s.fill((255, 255, 200))  # светлая вспышка
                screen.blit(s, self.flash_rect.topleft)
