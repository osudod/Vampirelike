
def start2(screen):
    
    import pygame
    
    running = True
    while running:
        screen.fill("#0000ff")
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()