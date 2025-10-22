
def play(screen):
    
    import pygame
    import sys
    from Buttons import Button
    from pygame_widgets.dropdown import Dropdown
    import pygame_widgets
    from Buttons import Button
    from level1 import start1
    import json
    
    THEME = "#984141"
    SCREEN_WIDTH = 800
    
    
    font_small = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 64)
    
    mas = {}
    with open("save.json") as file:
        mas = json.load(file)
    
    if mas["shop"]["bomber"] == "yes":
        dropdown_player = Dropdown(screen, 300, 200, 200, 50, name='-',choices=['Самурай','Стрелок','Подрывник'], colour=(255,0,0), values=[1, 2, 3], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
    else:
        dropdown_player = Dropdown(screen, 300, 200, 200, 50, name='-',choices=['Самурай','Стрелок'], colour=(255,0,0), values=[1, 2], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
    
    dropdown_stage = Dropdown(screen, 300, 300, 200, 50, name='-',choices=["Поляна", "Город"], colour=(255,0,0), values=[1, 2], direction='down', textColour=(255,255,255), textHAlign='centre', font=font_small)
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
                    # print(f"Player: {player} Stage: {stage}")
                    if player and stage:
                        start1(screen, stage, player)
        pygame_widgets.update(events)
        pygame.display.flip()