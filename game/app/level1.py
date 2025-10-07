
def start1(screen):
    
    import pygame
    
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
    
    # text_timer = font_large.render(text, True, "#ffffff")
    
    # text_timer_rect = text_timer.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    
    running = True
    while running:
        screen.fill("#00ff00")
        
        screen.blit(font_large.render(text, True, "#ffffff"), (SCREEN_WIDTH//2-85, 30))
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT: 
                timer += 1
                text = tran_time(timer) if timer <= 1800 else "30:00"
                
        pygame.display.flip()