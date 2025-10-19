
from random import randint, uniform
from Melee_zombie import Melee

class WaveManager:
    def __init__(self):
        self.current_wave = 1
        self.spawned_in_wave = 0
        self.monsters_per_wave = 30  # стартовое количество
        self.spawn_cooldown = 60     # кадров между спавном (60 = 1 сек при 60 FPS)
        self.last_spawn_time = 0
        self.wave_cleared = True

    def update(self, timer, monsters, spawn_points):
        # Если волна очищена — запускаем новую
        if self.wave_cleared:
            print(f"🔥 Волна {self.current_wave} началась!")
            self.wave_cleared = False
            self.spawned_in_wave = 0
            
        if self.spawned_in_wave < self.monsters_per_wave:
            loc = spawn_points[randint(0, 3)]
            monsters.append(Melee(
                image="../assets/enemes/New Piskel-1.png.png",
                damage=5 + self.current_wave,            # каждый раунд сильнее
                hp=50 + self.current_wave * 10,          # больше HP
                speed=uniform(0, 0.4 + self.current_wave * 0.05),  # скорость растет
                x=loc[0], y=loc[1]
            ))
            self.spawned_in_wave += 1
            self.last_spawn_time = timer

        # Проверяем, не убиты ли все монстры
        if self.spawned_in_wave >= self.monsters_per_wave and len(monsters) == 0:
            print(f"✅ Волна {self.current_wave} завершена!")
            self.current_wave += 1
            self.monsters_per_wave = int(self.monsters_per_wave * 1.4)  # растет
            self.wave_cleared = True
