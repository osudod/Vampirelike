def death_screen(screen, info):
    import pygame
    import sys, os
    from Buttons import Button
    from Save_manager import load_save, save_game, get_save_path

    player = info[0]
    kills = info[0].kills
    wave = info[1].current_wave
    level = info[0].level

    font_big = pygame.font.SysFont('Arial', 72)
    font_small = pygame.font.SysFont('Arial', 36)
    font_mid = pygame.font.SysFont('Arial', 48)

    # Кнопки
    retry_button = Button(50, 470, 280, 70, "Играть снова")
    menu_button = Button(360, 470, 200, 70, "В меню")
    exit_button = Button(610, 470, 150, 70, "Выход")

    def handle_click(pos):
        if retry_button.rect.collidepoint(pos):
            return "retry"
        if menu_button.rect.collidepoint(pos):
            return "menu"
        if exit_button.rect.collidepoint(pos):
            return "exit"
        return None

    # Затухание фона
    overlay = pygame.Surface((800, 600))
    overlay.fill((0, 0, 0))
    alpha = 0
    clock = pygame.time.Clock()

    # Мягкое затемнение
    for _ in range(30):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        alpha += 8
        clock.tick(30)

    # Основной цикл экрана смерти
    running = True
    while running:
        screen.fill("#000000")

        # Заголовок
        title = font_big.render("ВЫ ПОГИБЛИ", True, (255, 50, 50))
        title_rect = title.get_rect(center=(400, 120))
        screen.blit(title, title_rect)

        # Информация о статистике
        stats = [
            f"Убийств: {kills}",
            f"Волна: {wave}",
            f"Уровень: {level}",
            f"Здоровье: 0 / {getattr(player, 'max_hp', 0)}"
        ]

        for i, text in enumerate(stats):
            stat = font_mid.render(text, True, (230, 230, 230))
            screen.blit(stat, (200, 200 + i * 50))

        # Кнопки
        retry_button.draw(screen, font_small)
        menu_button.draw(screen, font_small)
        exit_button.draw(screen, font_small)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = handle_click(event.pos)
                try:
                    mas = load_save()
                except Exception:
                    print("Ошибка: сейв повреждён или принадлежит другому компьютеру.")
                    # Можно пересоздать новый сейв
                    os.remove(get_save_path())
                    mas = load_save()
                mas["kills"] = mas["kills"] + kills
                save_game(mas)
                if action == "retry":
                    return "retry"
                if action == "menu":
                    pygame.mixer.music.stop()
                    return "menu"
                if action == "exit":
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
