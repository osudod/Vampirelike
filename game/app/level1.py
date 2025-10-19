
def pause(screen, info):
    
    import pygame
    import sys
    from Buttons import Button
    
    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    escape_button = Button(50,50,210,70,"Назад в игру")
    menu_button = Button(300,50,230,70,"Выход в меню")
    
    
    
    def handle_menu_click(pos):
        if escape_button.rect.collidepoint(pos):
            return "назад"
        if menu_button.rect.collidepoint(pos):
            return "меню"

    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    
    info_title = font_large.render("Информация", True, "#ffffff")
    info_title_rect = info_title.get_rect(center=(400,160))
    
    text_player = font_small.render("Персонаж: ", True, "#ffffff")
    text_player_rect = text_player.get_rect(topleft=(50,220))
    
    if info[2] == 1:
        player = "Самурай"
    if info[2] == 2:
        player = "Стрелок"
    if info[2] == 3:
        player = "Подрывник"
    
    player_chois = font_small.render(player, True, "#ffffff")
    player_chois_rect = player_chois.get_rect(topleft=(210, 220))
    
    text_hp = font_small.render("Здоровье: ", True, "#ffffff")
    text_hp_rect = text_hp.get_rect(topleft=(50,250))
    
    player_hp = font_small.render(str(info[0].hp_actual), True, "#ffffff")
    player_hp_rect = player_hp.get_rect(topleft=(210, 250))
    
    
    running = True
    while running:
        screen.fill("#770000ff")
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    running = False
                if clicked_option == "меню":
                    pygame.mixer.music.stop()
                    return "меню"
        
        keys = pygame.key.get_pressed()
        
        escape_button.draw(screen,font_small)
        menu_button.draw(screen, font_small)
        
        screen.blit(info_title, info_title_rect)
        screen.blit(text_player, text_player_rect)
        screen.blit(player_chois, player_chois_rect)
        screen.blit(text_hp, text_hp_rect)
        screen.blit(player_hp, player_hp_rect)
        
        pygame.display.flip()

def start1(screen, stage, player):
    
    import pygame
    import sys
    from math import sqrt
    from Player import Player
    from Melee_zombie import Melee
    import json
    from random import randint, uniform, sample
    from Melee_player import MeleePlayer
    from GunPlayer import GunPlayer
    from BombPlayer import BombPlayer
    from ExplosionEffect import ExplosionEffect
    from WaveManaget import WaveManager
    
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
    
    def apply_cooldown_reduction(player, factor=0.8, min_cd=100):
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
        pygame.mixer.music.load("../assets/music/82872.mp3")
    if stage == 2:
        pygame.mixer.music.load("../assets/music/kino-less-than-i-used-to.mp3")
    mas = {}
    with open("save.json") as file:
            mas = json.load(file)
    music_volume = mas["music"]
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    spawn_mons = [(10, randint(250,350)),(randint(350,550), 10),(SCREEN_WIDTH - 50, randint(250,350)),(randint(450,550), SCREEN_HEIGHT- 50)]
    monsters = []
    
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = tran_time(timer)
    clock = pygame.time.Clock()
    
    x = 800 // 2
    y = 600 // 2
    if player == 1:
        image = "../assets/player/melee.png"
        dmg = 40
        hp = 100
        spd = 5
        player1 = MeleePlayer(image=image,damage=dmg, hp=hp, speed=spd, x=x, y=y)
    if player == 2:
        image = "../assets/player/gun.png"
        dmg = 30
        hp = 70
        spd = 3
        player1 = GunPlayer(image, dmg, hp, spd,x,y)
        bullets = []
    if player == 3:
        image = "../assets/player/bomber.png"
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
                            apply_cooldown_reduction(player1, factor=0.8, min_cd=500)

                        # закрываем меню
                        level_up_active = False
                        level_up_options = []
                # игнорируем остальные события во время меню
                continue
            if event.type == pygame.USEREVENT: 
                if mode == "play":
                    timer += 1
                    text = tran_time(timer) if timer <= 1800 else "30:00"
        
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_ESCAPE]:
            mode = "pause"
            valuy = pause(screen,[player1, wave, player, stage])
            if valuy == "меню":
                running = False
            mode = "play"
            
        
        # если активен левелап — рисуем меню и пропускаем апдейты
        if level_up_active:
            draw_level_up_menu(screen, level_up_options, font_large, font_small)
            pygame.display.flip()
            clock.tick(60)
            continue  # переходим к следующему кадру, остальная логика не выполняется
        
        
        player1.move(keys)
        
        if isinstance(player1, BombPlayer):
            player1.attack(monsters, bombs)
        
        player1.draw(screen=screen)
        
        
        if player == 1:
            player1.auto_attack(monsters)
            player1.draw_slash(screen)
        elif player == 2:
            player1.attack(monsters,bullets)
            for bullet in bullets[:]:
                if not bullet.update(monsters, player1):
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
                for m in monsters:
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
                            # print("💥 ВЗРЫВ! HP монстра:", m.hp_actual)
                            if m.hp_actual <= 0:
                                player1.xp += 10
                                player1.kills += 1
                                monsters.remove(m)
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

        wave.update(timer, monsters, spawn_mons)
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

        
        if player1.invincible:
            if pygame.time.get_ticks() - player1.last_hit_time >= player1.invincible_time:
                player1.invincible = False

        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        # рисуем верхнюю панель со статистикой
        draw_progress_ui(screen, player1.kills, player1.xp, player1.level, player1.xp_required, font_small)

        
        
        clock.tick(60)
        pygame.display.flip()