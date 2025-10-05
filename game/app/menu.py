
def play(screen):
    
    import pygame
    import sys
    from Buttons import Button
    from pygame_widgets.dropdown import Dropdown
    import pygame_widgets
    from Buttons import Button
    
    THEME = "#984141"
    SCREEN_WIDTH = 800
    
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    
    dropdown = Dropdown(screen, 300, 200, 200, 50, name='Select Player',choices=['Player1','Player2','Player3'], colour=(255,0,0), values=[1, 2, 3], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
    
    back_button_game = Button(40, 75, 100, 60,"Назад")
    
    title = font_large.render("Выбор игры", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    text = font_small.render("Персонаж", True, "#ffffff")
    text_rect = text.get_rect(center=(200, 220))
    
    def handle_menu_click(pos):
        if back_button_game.rect.collidepoint(pos):
            return "назад"
    
    running = True
    while running:
        screen.fill(THEME)
        
        screen.blit(title, title_rect)
        
        screen.blit(text, text_rect)
        
        back_button_game.draw(screen,font_small)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    running = False
                    dropdown.hide()
        
        
        
        pygame_widgets.update(events)
        pygame.display.flip()