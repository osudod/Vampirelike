
def draw_settings(screen):
    
    import pygame
    import sys, os
    import pygame_widgets
    from pygame_widgets.slider import Slider
    from Buttons import Button
    from Save_manager import load_save, save_game, get_save_path

    
    def resource_path(relative_path):
        """Возвращает путь к ресурсу (работает и в exe, и при разработке)"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    SCREEN_WIDTH = 800
    THEME = "#984141"

    pygame.mixer.music.load(resource_path("assets/music/keys-of-moon-lonesome-journey.mp3"))
    try:
        mas = load_save()
    except Exception:
        print("Ошибка: сейв повреждён или принадлежит другому компьютеру.")
        # Можно пересоздать новый сейв
        os.remove(get_save_path())
        mas = load_save()

    music_volume = mas["music"]
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)

    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    back_button_settings = Button(40, 75, 100, 60,"Назад")
    reset_button_settings = Button(300, 250, 400, 100,"Сбросить сохранение")
    title = font_large.render("Настройки", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    text_reset = font_small.render("Сбросить", True, "#ffffff")
    text_reset_rect = text_reset.get_rect(center=(160, 300))
    
    slider = Slider(screen, 250, 185, 200, 40, min=0, max=1, step=0.1, colour="#ffffff", handleColour=(200, 41, 9),valueColour=(90, 35, 35), initial=music_volume)
    
    sound_set = font_small.render("Музыка", True, "#ffffff")
    sound_set_rect = sound_set.get_rect(center=(160, 200))
    
    def handle_menu_click(pos):
        if back_button_settings.rect.collidepoint(pos):
            return "назад"
        if reset_button_settings.rect.collidepoint(pos):
            return "сброс"
        
    def save(music_vol):
        try:
            mas = load_save()
        except Exception:
            print("Ошибка: сейв повреждён или принадлежит другому компьютеру.")
            # Можно пересоздать новый сейв
            os.remove(get_save_path())
            mas = load_save()
        mas["music"] = music_vol
        save_game(mas)
        
    running = True
    while running:
        screen.fill(THEME)
    
        screen.blit(title, title_rect)
        screen.blit(text_reset, text_reset_rect)
        
        back_button_settings.draw(screen, font_small)
        reset_button_settings.draw(screen, font_small)
        
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
                if clicked_option == "сброс":
                    mas = {"music": 0.5, "kills": 0, "shop": {"bomber": "no", "healing": {"buy": "no", "level": 0}}}
                    save_game(mas)
        music_volume = slider.getValue()
        pygame.mixer.music.set_volume(music_volume)
        pygame_widgets.update(events)
        pygame.display.flip()
    
    