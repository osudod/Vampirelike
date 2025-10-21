
from random import randint, uniform
from Melee_zombie import Melee
from RangedZombie import RangedZombie
import pygame
import math

class WaveManager:
    def __init__(self):
        self.current_wave = 1
        self.spawned_in_wave = 0
        self.monsters_per_wave = 30  # стартовое количество
        self.spawn_cooldown = 60     # кадров между спавном (60 = 1 сек при 60 FPS)
        self.last_spawn_time = 0
        self.wave_cleared = True
        self.boss_active = False
        self.boss_intro_active = False
        self.boss_intro_start = 0
        self.boss_intro_duration = 2000  # 2 секунды показа анимации
        self.font = pygame.font.Font(None, 80) 

    def update(self, timer, monsters, spawn_points, ranged_zombies):
        # Если волна очищена — запускаем новую
        if self.wave_cleared:
            print(f"🔥 Волна {self.current_wave} началась!")
            self.wave_cleared = False
            self.spawned_in_wave = 0
            
        if self.current_wave % 5 == 0 and not self.boss_active:
            loc = spawn_points[randint(0, 3)]
            boss = Melee(
                image="../assets/enemes/New Piskel-1.png.png",  # можешь заменить на свою текстуру
                damage=10 + self.current_wave * 2,
                hp=400 + self.current_wave * 100,
                speed=0.5 + self.current_wave * 0.05,
                x=loc[0], y=loc[1]
            )
            boss.size_multiplier = 2.0  # можешь использовать для увеличения спрайта
            monsters.append(boss)
            self.boss_active = True
            self.boss_intro_active = True
            self.boss_intro_start = pygame.time.get_ticks()
            return  # ждём пока игрок убьёт босса
            
            
            
        if self.spawned_in_wave < self.monsters_per_wave:
            loc = spawn_points[randint(0, 3)]
            monsters.append(Melee(
                image="../assets/enemes/New Piskel-1.png.png",
                damage=5 + self.current_wave,            # каждый раунд сильнее
                hp=50 + self.current_wave * 10,          # больше HP
                speed=uniform(0, 0.4 + self.current_wave * 0.05),  # скорость растет
                x=loc[0], y=loc[1]
            ))
            # ranged_zombies.append(RangedZombie(
            #     "../assets/enemes/New Piskel(1).png",
            #     damage=5 + self.current_wave,
            #     hp=50 + self.current_wave * 10,
            #     speed=uniform(0, 0.3 + self.current_wave * 0.05),
            #     x=loc[0],
            #     y=loc[1]))
            self.spawned_in_wave += 1
            self.last_spawn_time = timer

        if self.current_wave % 5 == 0:
                    # волна с боссом завершается, когда босс убит
            if self.boss_active and len(monsters) == 0:
                print(f"🏆 Босс побеждён! Волна {self.current_wave} завершена!")
                self.current_wave += 1
                self.monsters_per_wave = int(self.monsters_per_wave * 1.3)
                self.wave_cleared = True
        # Проверяем, не убиты ли все монстры
        else:
            if self.spawned_in_wave >= self.monsters_per_wave and len(monsters) == 0 and len(ranged_zombies) == 0:
                print(f"✅ Волна {self.current_wave} завершена!")
                self.current_wave += 1
                self.monsters_per_wave = int(self.monsters_per_wave * 1.4)  # растет
                self.wave_cleared = True
                
    def draw_boss_intro(self, screen, width, height):
        if not self.boss_intro_active:
            return

        elapsed = pygame.time.get_ticks() - self.boss_intro_start
        if elapsed > self.boss_intro_duration:
            self.boss_intro_active = False
            return

        # полупрозрачная чёрная заливка
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # пульсирующий эффект надписи
        alpha = 200 + int(55 * math.sin(elapsed / 100))
        color = (255, 200, 50)
        text = self.font.render("BOSS WAVE", True, color)
        text.set_alpha(alpha)

        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)