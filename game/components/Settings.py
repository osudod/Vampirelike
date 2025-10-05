
def draw_settings(screen):
    
    import pygame
    import sys
    import os

    from ..components.Buttons import Button
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    THEME = "#984141"

    musc = pygame.mixer.music.load("game/assets/music/keys-of-moon-lonesome-journey.mp3")
    music_volume = 1
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)

    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    def handle_menu_click(pos):
        if back_button_settings.rect.collidepoint(pos):
            return "Назад"
        return None
    
    back_button_settings = Button(40,75,100,60,"Назад")
    title = font_large.render("Настройки", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    sound_set = font_small.render("Музыка", True, "#ffffff")
    sound_set_rect = sound_set.get_rect(center=(160, 200))
    
    running = True
    while running:
        screen.fill(THEME)
        back_button_settings.draw(screen=screen, font=font_small)
    
        screen.blit(title, title_rect)
        
        screen.blit(sound_set, sound_set_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "Назад":
                    running = False
        pygame.display.flip()

