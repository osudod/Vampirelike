import pygame

class Char:
    
    def __init__(self, image, damage, hp, speed, x, y):
        self.image = pygame.image.load(image)
        self.damage = damage
        self.hp = hp
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
    
    def draw(self, screen, x, y):
        screen.blit(self.image,(x, y))
    
    def attack(self, enemy):
        return enemy.hp - self.damage if enemy.hp  - self.damage >= 0 else 'overkill'
    
    def get_speed(self):
        return self.speed