import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed, damage):
        self.image = pygame.Surface((10, 4))  # можно заменить на спрайт пули
        self.image.fill((255, 255, 0))  # желтая пуля
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage

        # Вычисляем направление (вектор)
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1  # защита от деления на 0
        self.dir_x = dx / distance
        self.dir_y = dy / distance

    def update(self):
        # Движение пули
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        # Если ушла за экран — удалить
        if (self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or
            self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT):
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
