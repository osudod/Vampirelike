
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
    if player == 2:
        image = "../assets/player/gun.png"
        dmg = 10
        hp = 70
        spd = 3
    if player == 3:
        image = "../assets/player/bomber.png"
        dmg = 15
        hp = 30
        spd = 7
        
    player1 = Player(image=image,damage=dmg, hp=hp, speed=spd, x=x, y=y)
    speed = player1.get_speed()
    
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
        
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if x >= 6:
                x -= speed
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if x <= 764:
                x += speed
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if y >= 6:
                y -= speed
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if y <= 554:
                y += speed
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            if x >= 6 and y <=554:
                x -= speed - 1
                y += speed - 1
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            if x >= 6 and y >= 6:
                x -= speed - 1
                y -= speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            if x <= 764 and y <= 554:
                x += speed - 1
                y += speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            if x <= 764 and y >= 6:
                x += speed - 1
                y -= speed - 1
        
        
        if timer % 60 == 0 and timer != 0:
            loc = spawn_mons[randint(0,3)]
            monsters.append(Melee(image="../assets/enemes/New Piskel-1.png.png", damage=5, hp=50, speed=uniform(0,1),x=loc[0], y=loc[1]))
        
        player1.draw(screen=screen,x=x,y=y)
        
        if monsters:
            for i in monsters:
                i.draw(screen, i.x, i.y)
                i.move(x, y)
                monr = i.image.get_rect()
                monr.topleft = (i.x, i.y)
                pla = player1.image.get_rect()
                pla.topleft = (x, y)
                if monr.colliderect(pla):
                    if str(i.attack(player1)).isdigit():
                        player1.hp = i.attack(player1)
                    else:
                        print(i.attack(player1))
        
        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        
        
        clock.tick(60)
        pygame.display.flip()