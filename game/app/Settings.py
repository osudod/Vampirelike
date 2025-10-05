
def draw_settings(screen):
    
    import json
    import pygame
    import sys
    import os
    import pygame_widgets
    from pygame_widgets.slider import Slider
    from Buttons import Button
    
    
    SCREEN_WIDTH = 800
    THEME = "#984141"

    musc = pygame.mixer.music.load("../assets/music/keys-of-moon-lonesome-journey.mp3")
    mas = {}
    with open("save.json") as file:
            mas = json.load(file)
    music_volume = mas["music"]
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)

    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    back_button_settings = Button(40, 75, 100, 60,"Назад")
    title = font_large.render("Настройки", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    slider = Slider(screen, 250, 185, 200, 40, min=0, max=1, step=0.1, colour="#ffffff", handleColour=(200, 41, 9),valueColour=(90, 35, 35), initial=music_volume)
    
    sound_set = font_small.render("Музыка", True, "#ffffff")
    sound_set_rect = sound_set.get_rect(center=(160, 200))
    
    def handle_menu_click(pos):
        if back_button_settings.rect.collidepoint(pos):
            return "назад"
        
    def save(music_vol):
        mas = {}
        with open("save.json") as file:
            mas = json.load(file)
        mas["music"] = music_vol
        with open("save.json", 'w') as file:
            json.dump(mas, file)
        
    running = True
    while running:
        screen.fill(THEME)
    
        screen.blit(title, title_rect)
        
        back_button_settings.draw(screen, font_small)
        
        screen.blit(sound_set, sound_set_rect)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    running = False
                    pygame.mixer.music.stop()
                    save(music_volume)
        music_volume = slider.getValue()
        pygame.mixer.music.set_volume(music_volume)
        pygame_widgets.update(events)
        pygame.display.flip()
    
    