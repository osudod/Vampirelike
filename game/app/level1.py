
def start1(screen):
    
    import pygame
    import sys
    from math import sqrt
    from Player import Player
    from Melee_zombie import Melee
    
    def tran_time(timer):
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
        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT: 
                timer += 1
                text = tran_time(timer) if timer <= 1800 else "30:00"
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            x -= speed * (sqrt(1/5) / 10)
            y += speed * (sqrt(1/5) / 10)
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            x -= speed * (sqrt(1/5) / 10)
            y -= speed * (sqrt(1/5) / 10)
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            x += speed * (sqrt(1/5) / 10)
            y += speed * (sqrt(1/5) / 10)
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            x -= speed * (sqrt(1/5) / 10)
            y -= speed * (sqrt(1/5) / 10)
        
        player1.draw(screen=screen,x=x,y=y)
        
        clock.tick(60)
        pygame.display.flip()