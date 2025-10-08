
def start1(screen):
    
    import pygame
    import sys
    from math import sqrt
    
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
    
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = tran_time(timer)
    clock = pygame.time.Clock()
    
    player_image = pygame.image.load("../assets/player/New_Piskel.png").convert_alpha()
    speed = 5
    x = 800 // 2
    y = 500 // 2
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
            x -= speed * (1/sqrt(2))
            y += speed * (1/sqrt(2))
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            x -= speed * (1/sqrt(2))
            y -= speed * (1/sqrt(2))
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            x += speed * (1/sqrt(2))
            y += speed * (1/sqrt(2))
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            x -= speed * (1/sqrt(2))
            y -= speed * (1/sqrt(2))
        
        screen.blit(player_image,(x,y))
        
        clock.tick(60)
        pygame.display.flip()