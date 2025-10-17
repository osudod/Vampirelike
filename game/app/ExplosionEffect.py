import pygame

class ExplosionEffect:
    def __init__(self, x, y, radius, damage):
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.start_time = pygame.time.get_ticks()
        self.duration = 200  # эффект держится 0.2 сек
        self.done_damage = False  # чтобы нанести урон только 1 раз

    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.duration:
            return False
        return True

    def draw(self, screen):
        # рисуем взрыв как круг
        pygame.draw.circle(screen, (255, 150, 0), (self.x, self.y), self.radius, 3)
