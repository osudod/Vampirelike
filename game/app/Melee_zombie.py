from Character import Char
import pygame

class Melee(Char):
    
    def __init__(self, image, damage, hp, speed, x, y):
        self.image = pygame.image.load(image).convert_alpha()
        self.damage = damage
        self.hp = hp
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
    
    def draw(self, screen):
        return super().draw(screen)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    def get_speed(self):
        return super().get_speed()
    
    def move(self, x, y):
        if x > self.x:
            self.x = self.x + self.speed
            self.rect.x = self.x + self.speed
        elif x < self.x:
            self.x = self.x - self.speed
            self.rect.x = self.x - self.speed
        if y > self.y:
            self.y = self.y + self.speed
            self.rect.y = self.y + self.speed
        elif y < self.y:
            self.y = self.y - self.speed
            self.rect.y = self.y - self.speed
    
