
def play(screen):
    
    import pygame
    import sys
    from Buttons import Button
    from pygame_widgets.dropdown import Dropdown
    import pygame_widgets
    from Buttons import Button
    from level1 import start1
    from level2 import start2
    
    THEME = "#984141"
    SCREEN_WIDTH = 800
    
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    
    dropdown_player = Dropdown(screen, 300, 200, 200, 50, name='Select Player',choices=['Player1','Player2','Player3'], colour=(255,0,0), values=[1, 2, 3], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
    dropdown_stage = Dropdown(screen, 300, 300, 200, 50, name='Select Stage',choices=["Stage 1", "Stage 2"], colour=(255,0,0), values=[1, 2], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
    back_button_game = Button(40, 75, 100, 60,"Назад")
    play_button_game = Button(300, 500, 200, 80,"Играть")
    
    title = font_large.render("Выбор игры", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    text = font_small.render("Персонаж", True, "#ffffff")
    text_rect = text.get_rect(center=(200, 225))
    
    text1 = font_small.render("Этап", True, "#ffffff")
    text_rect1 = text.get_rect(center=(200, 325))
    
    def handle_menu_click(pos):
        if back_button_game.rect.collidepoint(pos):
            return "назад"
        elif play_button_game.rect.collidepoint(pos):
            return "играть"
    
    running = True
    while running:
        screen.fill(THEME)
        
        screen.blit(title, title_rect)
        
        screen.blit(text, text_rect)
        
        screen.blit(text1, text_rect1)
        
        back_button_game.draw(screen,font_small)
        
        play_button_game.draw(screen, font_small)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    running = False
                    dropdown_player.hide()
                    dropdown_stage.hide()
                if clicked_option == "играть":
                    player = dropdown_player.getSelected()
                    stage = dropdown_stage.getSelected()
                    print(f"Player: {player} Stage: {stage}")
                    if player and stage:
                        if stage == 1:
                            start1(screen)
                        elif stage == 2:
                            start2(screen)
                        # running = False
                        # dropdown_player.hide()
                        # dropdown_stage.hide()
        
        pygame_widgets.update(events)
        pygame.display.flip()