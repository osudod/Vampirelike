
def pause(screen):
    
    import pygame
    import sys
    from Buttons import Button
    
    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    escape_button = Button(50,50,210,70,"Назад в игру")
    menu_button = Button(50,150,230,70,"Выход в меню")
    
    def handle_menu_click(pos):
        if escape_button.rect.collidepoint(pos):
            return "назад"
        if menu_button.rect.collidepoint(pos):
            return "меню"

    
    running = True
    while running:
        screen.fill("#727272ff")
        
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
        
        pygame.display.flip()

def start1(screen, stage, player):
    
    import pygame
    import sys
    from math import sqrt
    from Player import Player
    from Melee_zombie import Melee
    import json
    from random import randint, uniform
    from Melee_player import MeleePlayer
    from GunPlayer import GunPlayer
    from BombPlayer import BombPlayer
    from ExplosionEffect import ExplosionEffect
    
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
    
    spawn_mons = [(10, SCREEN_HEIGHT // 2),(SCREEN_WIDTH // 2, 10),(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2),(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)]
    monsters = []
    
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = tran_time(timer)
    clock = pygame.time.Clock()
    
    x = 800 // 2
    y = 600 // 2
    if player == 1:
        image = "../assets/player/melee.png"
        dmg = 1
        hp = 100
        spd = 5
        player1 = MeleePlayer(image=image,damage=dmg, hp=hp, speed=spd, x=x, y=y)
    if player == 2:
        image = "../assets/player/gun.png"
        dmg = 10
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
            if event.type == pygame.USEREVENT: 
                if mode == "play":
                    timer += 1
                    text = tran_time(timer) if timer <= 1800 else "30:00"
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            mode = "pause"
            valuy = pause(screen)
            if valuy == "меню":
                running = False
            mode = "play"
            
        

        
        
        if timer % 60 == 0:
            loc = spawn_mons[randint(0,3)]
            monsters.append(Melee(image="../assets/enemes/New Piskel-1.png.png", damage=5, hp=50, speed=uniform(0,0.6),x=loc[0], y=loc[1]))
        
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
                if not bullet.update(monsters):
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
                            print("💥 ВЗРЫВ! HP монстра:", m.hp_actual)
                    exp.done_damage = True
                    
            for bomb in bombs:
                bomb.draw(screen)

            for exp in explosions:
                exp.draw(screen)
            

        if monsters:
            for i in monsters:
                i.move(player1.rect, monsters)
                i.draw(screen)
                monr = i.rect
                pla = player1.rect
                if monr.colliderect(pla):
                    if str(i.attack(player1)).isdigit():
                        player1.hp = i.attack(player1)
        
        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        
        
        clock.tick(60)
        pygame.display.flip()