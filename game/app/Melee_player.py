import pygame
from Player import Player  # или напрямую из Character, если хочешь

class MeleePlayer(Player):
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)

        # Параметры автоатаки
        self.attack_cooldown = 2000  # каждые 2 секунды
        self.last_attack_time = pygame.time.get_ticks()

        # Эффект удара
        self.slash_rect = None
        self.slash_show_time = 100  # 0.1 сек
        self.slash_created_time = 0

    def auto_attack(self, monsters):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.slash_attack(monsters)   # Урон монстрам
            self.create_slash_effect()   # Эффект удара

    def slash_attack(self, monsters):
        slash_rect = pygame.Rect(self.rect.x, self.rect.y, 60, 60)
        slash_rect.topleft = (self.rect.topleft[0] + 50, self.rect.topleft[1])  # Удар вправо (можно потом сделать направление)
        
        for monster in monsters:
            if slash_rect.colliderect(monster.rect):
                monster.hp -= self.damage
                print("⚔ Удар мечом! HP монстра:", monster.hp)

    def create_slash_effect(self):
        self.slash_rect = pygame.Rect(self.rect.x, self.rect.y, 60, 60)
        self.slash_rect.topleft = (self.rect.topleft[0] + 50, self.rect.topleft[1])
        self.slash_created_time = pygame.time.get_ticks()

    def draw_slash(self, screen):
        if self.slash_rect:
            if pygame.time.get_ticks() - self.slash_created_time > self.slash_show_time:
                self.slash_rect = None
            else:
                s = pygame.Surface((self.slash_rect.width, self.slash_rect.height))
                s.set_alpha(120)
                s.fill((255, 50, 50))  # Можно заменить на текстуру удара
                screen.blit(s, self.slash_rect.topleft)
