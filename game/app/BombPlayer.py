import pygame
from Player import Player
from Bomb import Bomb
from ExplosionEffect import ExplosionEffect

class BombPlayer(Player):
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
        self.cooldown = 3000  # 3 секунды
        self.last_throw = pygame.time.get_ticks()
        self.explosion_radius = 80

    def attack(self, monsters, bombs):
        if not monsters:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw < self.cooldown:
            return

        # Ищем ближайшего монстра
        nearest = min(monsters, key=lambda m: ((m.rect.x - self.rect.x)**2 + (m.rect.y - self.rect.y)**2))

        # Создаем бомбу
        bomb_speed = self.speed + 1  # медленнее пули
        bombs.append(Bomb(self.rect.centerx, self.rect.centery, nearest.rect.centerx, nearest.rect.centery, bomb_speed, self.damage, self.explosion_radius))

        self.last_throw = pygame.time.get_ticks()
