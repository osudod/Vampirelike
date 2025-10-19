import pygame
from Player import Player  # или напрямую из Character, если хочешь

class MeleePlayer(Player):
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
        self.last_dir = "right" 

        # Параметры автоатаки
        self.attack_cooldown = 2000  # каждые 2 секунды
        self.last_attack_time = pygame.time.get_ticks()

        # Эффект удара
        self.slash_rect = None
        self.slash_show_time = 100  # 0.1 сек
        self.slash_created_time = 0
    
    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.last_dir = "right"
        elif keys[pygame.K_LEFT]:
            self.last_dir = "left"
        if keys[pygame.K_UP]:
            self.last_dir = "up"
        elif keys[pygame.K_DOWN]:
            self.last_dir = "down"
        return super().move(keys)

    def auto_attack(self, monsters):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.slash_attack(monsters)   # Урон монстрам
            self.create_slash_effect()   # Эффект удара


    def slash_attack(self, monsters):
        slash_rect = pygame.Rect(self.rect.x, self.rect.y, 60, 60)
        if self.last_dir == "right":
            slash_rect.midleft = self.rect.midright
        elif self.last_dir == "left":
            slash_rect.midright = self.rect.midleft
        elif self.last_dir == "up":
            slash_rect.midbottom = self.rect.midtop
        elif self.last_dir == "down":
            slash_rect.midtop = self.rect.midbottom
        
        
        for monster in monsters:
            if slash_rect.colliderect(monster.rect):
                monster.hp_actual -= self.damage
                # print("⚔ Удар мечом! HP монстра:", monster.hp_actual)
                if monster.hp_actual <= 0:
                    monsters.remove(monster)
                    self.xp += 10
                    self.kills += 1
                

    def create_slash_effect(self):
        self.slash_rect = pygame.Rect(self.rect.x, self.rect.y, 60, 60)
        if self.last_dir == "right":
            self.slash_rect.midleft = self.rect.midright
        elif self.last_dir == "left":
            self.slash_rect.midright = self.rect.midleft
        elif self.last_dir == "up":
            self.slash_rect.midbottom = self.rect.midtop
        elif self.last_dir == "down":
            self.slash_rect.midtop = self.rect.midbottom
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
