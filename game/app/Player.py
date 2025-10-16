from Character import Char
import pygame

class Player(Char):
    
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
    
    def draw(self, screen, x, y):
        return super().draw(screen, x, y)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    def get_speed(self):
        return super().get_speed()
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6:
                self.rect.x -= self.speed
                return self.rect.x, self.rect.y
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764:
                self.rect.x += self.speed
                return self.rect.x, self.rect.y
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if self.rect.y >= 6:
                self.rect.y -= self.speed
                return self.rect.x, self.rect.y
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if self.rect.y <= 554:
                self.rect.y += self.speed
                return self.rect.x, self.rect.y
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6 and self.rect.y <=554:
                self.rect.x -= self.speed - 1
                self.rect.y += self.speed - 1
                return self.rect.x, self.rect.y
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if self.rect.x >= 6 and self.rect.y >= 6:
                self.rect.x -= self.speed - 1
                self.rect.y -= self.speed - 1
                return self.rect.x, self.rect.y
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764 and self.rect.y <= 554:
                self.rect.x += self.speed - 1
                self.rect.y += self.speed - 1
                return self.rect.x, self.rect.y
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if self.rect.x <= 764 and self.rect.y >= 6:
                self.rect.x += self.speed - 1
                self.rect.y -= self.speed - 1
                return self.rect.x, self.rect.y
        return self.rect.x, self.rect.y
    