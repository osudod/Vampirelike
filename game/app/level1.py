
def start1(screen):
    
    import pygame
    import sys
    from math import sqrt
    from Player import Player
    from Melee_zombie import Melee
    import json
    from random import randint
    
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
    
    def collide_mon(monsters):
        if len(monsters) > 0:
            for monster in monsters:
                if player1.rect.collidepoint(monster.rect.center):
                    if str(monster.attack(player1)).isdigit():
                        player1.hp = monster.attack(player1)
    
    pygame.mixer.music.load("../assets/music/82872.mp3")
    mas = {}
    with open("save.json") as file:
            mas = json.load(file)
    music_volume = mas["music"]
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    SCREEN_WIDTH = 800
    
    monsters = []
    
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = tran_time(timer)
    clock = pygame.time.Clock()
    
    x = 800 // 2
    y = 600 // 2
    player1 = Player(image="../assets/player/New_Piskel.png",damage=1, hp=100, speed=5)
    speed = player1.get_speed()
    motion = "stop"
    
    running = True
    while running:
        screen.fill("#4a964a")
        
        
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT: 
                timer += 1
                text = tran_time(timer) if timer <= 1800 else "30:00"
        
        keys = pygame.key.get_pressed()
        
        
        
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            x -= speed
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            x += speed
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            y -= speed
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            y += speed
            print(player1.hp)
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            x -= speed - 1
            y += speed - 1
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            x -= speed - 1
            y -= speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            x += speed - 1
            y += speed - 1
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
            x += speed - 1
            y -= speed - 1
        
        
        if timer % 60 == 0 and timer != 0:
            monsters.append(Melee(image="../assets/enemes/New Piskel-1.png.png", damage=5, hp=50, speed=3))
        
        player1.draw(screen=screen,x=x,y=y)
        
        if monsters:
            for i in monsters:
                i.draw(screen, randint(0, 799), randint(0,599))
        
        collide_mon(monsters)
        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        
        
        clock.tick(60)
        pygame.display.flip()