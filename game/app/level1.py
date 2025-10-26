
def pause(screen, info):
    import pygame
    import sys
    from Buttons import Button
    
    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)

    escape_button = Button(50, 500, 210, 70, "Назад в игру")
    menu_button = Button(300, 500, 230, 70, "Выход в меню")

    def handle_menu_click(pos):
        if escape_button.rect.collidepoint(pos):
            return "назад"
        if menu_button.rect.collidepoint(pos):
            return "меню"

    # === Извлекаем данные ===
    player_obj = info[0]
    wave = info[1]
    player_id = info[2]

    # Имя персонажа
    if player_id == 1:
        player_name = "Самурай"
    elif player_id == 2:
        player_name = "Стрелок"
    elif player_id == 3:
        player_name = "Подрывник"
    else:
        player_name = "Неизвестно"

    # HP
    if hasattr(player_obj, "hp_actual"): 
        current_hp = int(player_obj.hp_actual)
    else:
        current_hp = int(player_obj.hp)

    max_hp = getattr(player_obj, "max_hp", current_hp)

    # Урон
    damage = getattr(player_obj, "damage", 0)

    # Скорость
    speed = getattr(player_obj, "speed", 0)

    # КД (ищем правильное поле)
    if hasattr(player_obj, "attack_cooldown"):
        cd_value = player_obj.attack_cooldown
    elif hasattr(player_obj, "cooldown"):
        cd_value = player_obj.cooldown
    else:
        cd_value = None

    running = True
    while running:
        screen.fill("#550000")

        # === Заголовок ===
        title = font_large.render("Пауза", True, "#ffffff")
        screen.blit(title, (300, 50))

        # === Информационный блок ===
        info_lines = [
            f"Персонаж: {player_name}",
            f"Волна: {wave.current_wave}",
            f"HP: {current_hp} / {max_hp}",
            f"Урон: {damage}",
            f"Скорость: {speed}"
        ]

        if cd_value:
            cd_sec = round(cd_value / 1000, 4)  # мс → секунды
            info_lines.append(f"КД: {cd_sec} сек")

        # Рисуем каждую строку
        for i, text in enumerate(info_lines):
            line = font_small.render(text, True, "#ffffff")
            screen.blit(line, (50, 150 + i * 40))

        # === Кнопки ===
        escape_button.draw(screen, font_small)
        menu_button.draw(screen, font_small)

        # === Обработка событий ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    return "назад"
                if clicked_option == "меню":
                    pygame.mixer.music.stop()
                    return "меню"

        pygame.display.flip()


def start1(screen, stage, player):
    
    import pygame
    import sys
    from math import sqrt
    from Player import Player
    from Melee_zombie import Melee
    from random import randint, uniform, sample
    from Melee_player import MeleePlayer
    from GunPlayer import GunPlayer
    from BombPlayer import BombPlayer
    from ExplosionEffect import ExplosionEffect
    from WaveManaget import WaveManager
    from DeathScreen import death_screen
    import os
    from Save_manager import load_save, get_save_path
    
    def resource_path(relative_path):
        """Получает путь к ресурсу при запуске из exe"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def draw_level_up_menu(screen, level_up_options, font_big, font_small):
        """
        Отрисовать полупрозрачное меню выбора апгрейда (VS-style).
        level_up_options — список 3 элементов (id, текст).
        """
        W, H = 800, 600  # если у тебя другие константы — подгони
        overlay = pygame.Surface((W, H))
        overlay.set_alpha(200)
        overlay.fill((10, 10, 10))
        screen.blit(overlay, (0, 0))

        # меню-рамка
        box_w, box_h = 560, 320
        box_x = (W - box_w) // 2
        box_y = (H - box_h) // 2
        pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, (200, 200, 200), (box_x, box_y, box_w, box_h), 3)

        # Заголовок
        title = font_small.render("ВЫБЕРИТЕ УЛУЧШЕНИЕ", True, (255, 215, 0))
        screen.blit(title, (box_x + 60, box_y + 20))
        font_small1 = pygame.font.SysFont('Arial', 16)
        # Опции
        for i, opt in enumerate(level_up_options):
            idx = i + 1
            text = f"[{idx}] {opt[1]}"
            opt_surf = font_small.render(text, True, (255, 255, 255))
            # Блок опции (декоративный)
            opt_box_x = box_x + 40
            opt_box_y = box_y + 90 + i * 70
            opt_box_w = box_w - 80
            opt_box_h = 56
            pygame.draw.rect(screen, (45, 45, 45), (opt_box_x, opt_box_y, opt_box_w, opt_box_h))
            pygame.draw.rect(screen, (100, 100, 100), (opt_box_x, opt_box_y, opt_box_w, opt_box_h), 2)
            screen.blit(opt_surf, (opt_box_x + 12, opt_box_y + 8))

        # Подсказка
        hint = font_small1.render("Нажмите 1 / 2 / 3 чтобы выбрать. Игра возобновится.", True, (200, 200, 200))
        screen.blit(hint, (box_x + 40, box_y + box_h - 40))
    
    def apply_cooldown_reduction(player, factor=0.8, min_cd=10):
        """
        Универсально уменьшает любую известную переменную перезарядки у игрока
        (attack_cooldown, cooldown, т.п.). Бережно: не опустим ниже min_cd (ms).
        """
        names = ["attack_cooldown", "cooldown", "attack_cd", "reload_time"]
        for n in names:
            if hasattr(player, n):
                cur = getattr(player, n)
                try:
                    new = max(int(cur * factor), min_cd)
                except Exception:
                    # если значение хранится в секундах — попробуем float
                    try:
                        new = max(cur * factor, min_cd/1000.0)
                    except Exception:
                        continue
                setattr(player, n, new)

    def build_random_level_options():
        """
        Возвращает 3 случайных опции из полного списка (4).
        Каждая опция — кортеж (id, текст).
        """
        all_opts = [
            ("dmg", "+10 УРОН"),
            ("spd", "+1 СКОРОСТЬ"),
            ("hp", "+30 HP и ЛЕЧЕНИЕ"),
            ("cd", "Быстрее атаки (-20% КД)")  # отображаемый текст по твоей просьбе
        ]
        # случайно выбираем 3 без повторов
        return sample(all_opts, 3)

    def draw_progress_ui(screen, kills, xp, level, xp_required, font_small):
        """
        Рисует верхнюю информационную панель: Kills / XP / LVL
        font_small — pygame.font объект, передать тот, который используешь
        """
        text = f"Kills: {kills}   |   XP: {xp} / {xp_required}   |   LVL: {level}"
        surf = font_small.render(text, True, (255, 255, 255))
        screen.blit(surf, (12, 8))
        
    def tran_time(timer):
        '''Transfer time(seconds) -> time(00:00)'''
        if len(str(timer)) == 1 and timer < 60:
            return f"00:0{str(timer)}"
        elif len(str(timer)) == 2 and timer < 60:
            return f"00:{str(timer)}"
        else:
            minu, sec = timer // 60, timer % 60
            if len(str(minu)) == 1:
                minu = '0' + str(minu)
            if len(str(sec)) == 1:
                sec = '0' + str(sec)
            return f"{minu}:{sec}"
    
    if stage == 1:
        pygame.mixer.music.load(resource_path("assets/music/82872.mp3"))
    if stage == 2:
        pygame.mixer.music.load(resource_path("assets/music/kino-less-than-i-used-to.mp3"))
    try:
        mas = load_save()
    except Exception:
        print("Ошибка: сейв повреждён или принадлежит другому компьютеру.")
        # Можно пересоздать новый сейв
        os.remove(get_save_path())
        mas = load_save()
    music_volume = mas["music"]
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    spawn_mons = [(10, randint(250,350)),(randint(350,550), 10),(SCREEN_WIDTH - 50, randint(250,350)),(randint(450,550), SCREEN_HEIGHT- 50)]
    monsters = []
    ranged_zombies = []
    enemy_bullets = []
    
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = tran_time(timer)
    clock = pygame.time.Clock()
    
    x = 800 // 2
    y = 600 // 2
    if player == 1:
        image = resource_path("assets/player/melee.png")
        dmg = 40
        hp = 100
        spd = 5
        player1 = MeleePlayer(image=image,damage=dmg, hp=hp, speed=spd, x=x, y=y)
    if player == 2:
        image = resource_path("assets/player/gun.png")
        dmg = 30
        hp = 70
        spd = 3
        player1 = GunPlayer(image, dmg, hp, spd,x,y)
        bullets = []
    if player == 3:
        image = resource_path("assets/player/bomber.png")
        dmg = 15
        hp = 30
        spd = 7
        player1 = BombPlayer(image, dmg, hp, spd,x,y)
        bombs = []
        explosions = []
    mode = "play"
    running = True
    
    
    level_up_active = False  # Когда TRUE — игра ставится на паузу
    level_up_options = [] 
    
    wave = WaveManager()
    
    if mas["shop"]["healing"]["buy"] == "yes":
        player1.regen = mas["shop"]["healing"]["level"]
    
    
    while running:
        if stage == 1:
            screen.fill("#4a964a")
        if stage == 2:
            screen.fill("#4a5596")
        
        
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if level_up_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        chosen = level_up_options[0][0]  # id опции
                    elif event.key == pygame.K_2:
                        chosen = level_up_options[1][0]
                    elif event.key == pygame.K_3:
                        chosen = level_up_options[2][0]
                    else:
                        chosen = None

                    if chosen:
                        # применяем эффект
                        if chosen == "dmg":
                            player1.damage = getattr(player1, "damage", 1) + 10
                        elif chosen == "spd":
                            player1.speed = getattr(player1, "speed", 1) + 1
                        elif chosen == "hp":
                            # обеспечим наличие max_hp
                            if not hasattr(player1, "max_hp"):
                                player1.max_hp = getattr(player1, "hp", 100)
                            player1.max_hp += 30
                            # лечим игрока полностью
                            if hasattr(player1, "hp_actual"):
                                player1.hp_actual = player1.max_hp
                            else:
                                setattr(player1, "hp_actual", player1.max_hp)
                        elif chosen == "cd":
                            apply_cooldown_reduction(player1, factor=0.8, min_cd=10)

                        # закрываем меню
                        level_up_active = False
                        level_up_options = []
                # игнорируем остальные события во время меню
                continue
            if event.type == pygame.USEREVENT: 
                if mode == "play":
                    timer += 1
        
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_ESCAPE]:
            mode = "pause"
            valuy = pause(screen,[player1, wave, player, stage])
            if valuy == "меню":
                running = False
                pygame.mixer.music.stop()
            mode = "play"
            
        
        # если активен левелап — рисуем меню и пропускаем апдейты
        if level_up_active:
            draw_level_up_menu(screen, level_up_options, font_large, font_small)
            pygame.display.flip()
            clock.tick(60)
            continue  # переходим к следующему кадру, остальная логика не выполняется
        
        
        player1.move(keys)
        
        if isinstance(player1, BombPlayer):
            player1.attack(monsters, bombs, ranged_zombies)
        
        player1.draw(screen=screen)
        
        if player1.regen != 0:
            current_time1 = pygame.time.get_ticks()
            if current_time1 - player1.last_regen >= player1.regen_cooldown:
                player1.last_regen = current_time1
                if player1.hp_actual < player1.max_hp:
                    player1.hp_actual = min(player1.hp_actual + player1.regen, player1.max_hp)
        
        
        if player == 1:
            player1.auto_attack(monsters, ranged_zombies)
            player1.draw_slash(screen)
        elif player == 2:
            player1.attack(monsters,bullets, ranged_zombies)
            for bullet in bullets[:]:
                if not bullet.update(monsters, player1, ranged_zombies):
                    bullets.remove(bullet)
            for bullet in bullets:
                bullet.draw(screen)
            if hasattr(player1, "draw_flash"):
                player1.draw_flash(screen)
        elif player == 3:
            for bomb in bombs[:]:
                if not bomb.update():
                    bombs.remove(bomb)
                    continue

                # Проверка столкновения с монстрами
                if monsters:
                    for m in monsters:
                        if bomb.rect.colliderect(m.rect):  # взрыв!
                            explosions.append(ExplosionEffect(bomb.rect.centerx, bomb.rect.centery, bomb.explosion_radius, bomb.damage))
                            bombs.remove(bomb)
                            break
                if ranged_zombies:
                    for m in ranged_zombies:
                        if bomb.rect.colliderect(m.rect):  # взрыв!
                            explosions.append(ExplosionEffect(bomb.rect.centerx, bomb.rect.centery, bomb.explosion_radius, bomb.damage))
                            bombs.remove(bomb)
                            break
            for exp in explosions[:]:
                if not exp.update():
                    explosions.remove(exp)
                    continue

                if not exp.done_damage:
                    for m in monsters:
                        dist = ((m.rect.centerx - exp.x)**2 + (m.rect.centery - exp.y)**2)**0.5
                        if dist <= exp.radius:
                            m.hp_actual -= exp.damage
                            if m.hp_actual <= 0:
                                player1.xp += 10
                                player1.kills += 1
                                monsters.remove(m)
                    exp.done_damage = True
                    for m in ranged_zombies:
                        dist = ((m.rect.centerx - exp.x)**2 + (m.rect.centery - exp.y)**2)**0.5
                        if dist <= exp.radius:
                            m.hp_actual -= exp.damage
                            if m.hp_actual <= 0:
                                player1.xp += 10
                                player1.kills += 1
                                ranged_zombies.remove(m)
                    exp.done_damage = True
                    
            for bomb in bombs:
                bomb.draw(screen)

            for exp in explosions:
                exp.draw(screen)
            
        if player1.xp >= player1.xp_required:
            level_up_active = True
            player1.xp -= player1.xp_required
            player1.xp_required = int(player1.xp_required * 1.4)  # XP растёт
            player1.level += 1
            level_up_options = build_random_level_options()

        wave.update(timer, monsters, spawn_mons, ranged_zombies)
        
        if monsters:
            for i in monsters:
                i.move(player1.rect, monsters)
                i.draw(screen)
                monr = i.rect
                pla = player1.rect
                if monr.colliderect(pla):
                    current_time = pygame.time.get_ticks()
                    if not player1.invincible:  # урон можно получить только если не неуязвим
                        player1.hp_actual -= i.damage
                        player1.invincible = True
                        player1.last_hit_time = current_time

        if ranged_zombies:
            for enemy in ranged_zombies:
                enemy.move_and_attack(player1.rect, player1.rect.center, enemy_bullets, ranged_zombies)
                enemy.draw(screen)
            
        for bullet in enemy_bullets[:]:
            bullet.update()
            bullet.draw(screen)

            # Проверка попадания в игрока
            if bullet.rect.colliderect(player1.rect):
                current_time = pygame.time.get_ticks()
                if not player1.invincible:  # если не в i-frame
                    player1.hp_actual -= bullet.damage
                    player1.invincible = True
                    player1.last_hit_time = current_time
                enemy_bullets.remove(bullet)
                continue

            # Удаление пуль, если ушли за экран
            if bullet.rect.x < -10 or bullet.rect.x > 810 or bullet.rect.y < -10 or bullet.rect.y > 610:
                enemy_bullets.remove(bullet)
                
        if player1.invincible:
            if pygame.time.get_ticks() - player1.last_hit_time >= player1.invincible_time:
                player1.invincible = False

        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        # screen.blit(images,images_rect)
        
        # рисуем верхнюю панель со статистикой
        draw_progress_ui(screen, player1.kills, player1.xp, player1.level, player1.xp_required, font_small)

        if player1.hp_actual <= 0:
            val = death_screen(screen, [player1, wave])
            if val == "retry":
                return start1(screen, stage, player)   # перезапуск уровня
            elif val == "menu":
                running = False   # возврат в главное меню
            elif val == "exit":
                pygame.quit()
                sys.exit()

        
        wave.draw_boss_intro(screen, 800, 600)
        clock.tick(60)
        pygame.display.flip()