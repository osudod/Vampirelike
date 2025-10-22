


def shop(screen):
    
    import pygame
    from Buttons import Button
    import json
    import sys
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    THEME = "#984141"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dead world")
        

    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 32)
    
    mas = {}
    with open("save.json") as file:
        mas = json.load(file)
        
    back_button_settings = Button(40, 75, 100, 60,"Назад")
    
    if mas["shop"]["healing"]["level"] < 5:
        buy_healing_button = Button(600, 250, 140, 90, "Купить")
    
    if mas["shop"]["bomber"] != "yes":
        buy_bomber_button = Button(600, 400, 140, 90, "Купить")
    
    

    text_kills = font_small.render("Убийства:", True, "#ffffff")
    text_kills_rect = text_kills.get_rect(topleft=(150,170))
    
    # text_kills_count = font_small.render(str(mas["kills"]).ljust(20,' '), True, "#ffffff")
    # text_kills_count_rect = text_kills_count.get_rect(topleft=(300, 170))

    text_heal = font_small.render("Регенерация", True, "#ffffff")
    text_heal_rect = text_heal.get_rect(topleft=(100,250))
    
    text_heal_level = font_small.render(f"уровень {mas["shop"]["healing"]["level"]}", True, "#ffffff")
    text_heal_level_rect = text_heal.get_rect(topleft=(100,293))
    
    text_heal_level_req = font_small.render(f"30 000 убийств 1 улучшение", True, "#ffffff")
    text_heal_level_req_rect = text_heal.get_rect(topleft=(100,340))
    
    text_bomb = font_small.render("Подрывник", True, "#ffffff")
    text_bomb_rect = text_bomb.get_rect(topleft=(100,400))
    
    # text_bomb_buy = font_small.render("есть" if mas["shop"]["bomber"] == "yes" else "нету", True, "#ffffff")
    # text_bomb_buy_rect = text_bomb_buy.get_rect(topleft=(100, 440))
    
    text_bomb_buy_req = font_small.render("100 000 убийств открытие", True, "#ffffff")
    text_bomb_buy_req_rect = text_bomb_buy_req.get_rect(topleft=(100, 480))

    def handle_menu_click(pos):
        if back_button_settings.rect.collidepoint(pos):
            return "назад"
        if mas["shop"]["healing"]["level"] < 5:
            if buy_healing_button.rect.collidepoint(pos):
                return "лечение"
        if mas["shop"]["bomber"] != "yes":
            if buy_bomber_button.rect.collidepoint(pos):
                return "подрывник"
        
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_option = handle_menu_click(event.pos)
                if clicked_option == "назад":
                    running = False
                if clicked_option == "лечение":
                    amount = mas["kills"]
                    lvl = mas["shop"]["healing"]["level"]
                    cond = mas["shop"]["healing"]["buy"]
                    if amount >= 30000:
                        amount -= 30000
                        lvl += 1
                        cond = "yes"
                    mas["kills"] = amount
                    mas["shop"]["healing"]["level"] = lvl
                    mas["shop"]["healing"]["buy"] = cond
                    with open("save.json", "w") as file:
                        json.dump(mas, file)
                if clicked_option == "подрывник":
                    amount = mas["kills"]
                    cond = mas["shop"]["bomber"]
                    if amount >= 100000:
                        amount -= 100000
                        cond = "yes"
                    mas["shop"]["bomber"] = cond
                    mas["kills"] = amount
                    with open("save.json", "w") as file:
                        json.dump(mas, file)
        screen.fill(THEME) 
        
        title = font_large.render("Магазин", True, "#ffffff")
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        
        back_button_settings.draw(screen, font_small)
        if mas["shop"]["bomber"] != "yes":
            buy_bomber_button.draw(screen, font_small)
        if mas["shop"]["healing"]["level"] < 5:
            buy_healing_button.draw(screen, font_small)
        
        screen.blit(title, title_rect)
        
        screen.blit(text_kills, text_kills_rect)
        
        screen.blit(font_small.render(str(mas["kills"]).ljust(20,' '), True, "#ffffff"), font_small.render(str(mas["kills"]).ljust(20,' '), True, "#ffffff").get_rect(topleft=(300, 170)))
        
        screen.blit(text_heal, text_heal_rect)
        
        screen.blit(font_small.render(f"уровень {mas["shop"]["healing"]["level"]}", True, "#ffffff"), font_small.render(f"уровень {mas["shop"]["healing"]["level"]}", True, "#ffffff").get_rect(topleft=(100,293)))
        
        screen.blit(text_heal_level_req, text_heal_level_req_rect)
        
        screen.blit(text_bomb, text_bomb_rect)
        
        screen.blit(font_small.render("есть" if mas["shop"]["bomber"] == "yes" else "нету", True, "#ffffff"), font_small.render("есть" if mas["shop"]["bomber"] == "yes" else "нету", True, "#ffffff").get_rect(topleft=(100, 440)))
        
        screen.blit(text_bomb_buy_req,text_bomb_buy_req_rect)

        pygame.display.flip()