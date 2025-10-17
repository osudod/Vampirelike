import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Bomb:
    def __init__(self, x, y, target_x, target_y, speed, damage, explosion_radius):
        self.image = pygame.Surface((14, 14))
        self.image.fill((200, 50, 50))  # красная граната
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage
        self.explosion_radius = explosion_radius

        # Направление движения
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0: dist = 1
        self.dir_x = dx / dist
        self.dir_y = dy / dist

        self.active = True  # пока летит — True, при столкновении — False

    def update(self):
        if not self.active:
            return False

        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        # удаляем, если вышла за экран
        if (self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or
            self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT):
            return False

        return True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
