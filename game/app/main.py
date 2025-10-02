
import os
import sys

if not __package__:
    __package__ = (
        (lambda p, n:
        (".".join(p[-n:]), sys.path.insert(0, os.sep.join(p[:-n])))[0])(
            os.path.realpath(__file__).split(os.sep)[:-1], 2))

import pygame
import level1
from ..assets.components.Buttons import Button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
THEME = "#984141"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dead world")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont('Arial', 64)
font_small = pygame.font.SysFont('Arial', 32)


play_button = Button(250, 200, 300, 60, "Играть")
settings_button = Button(250, 300, 300, 60, "Настройки")
exit_button = Button(250, 400, 300, 60, "Выход")

back_button_settings = Button(40,75,100,60,"Назад")

def draw_menu():
    screen.fill(THEME) 
    
    title = font_large.render("Dead world", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    play_button.draw(screen=screen, font=font_small)
    settings_button.draw(screen=screen, font=font_small)
    exit_button.draw(screen=screen, font=font_small)
    
    screen.blit(title, title_rect)
    
    pygame.display.flip()

def draw_settings():
    screen.fill("#984141")
    
    title = font_large.render("Настройки", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    back_button_settings.draw(screen=screen, font=font_small)
    
    screen.blit(title, title_rect)
    
    pygame.display.flip()

def handle_menu_click(pos):
    if play_button.rect.collidepoint(pos):
        return "играть"
    elif settings_button.rect.collidepoint(pos):
        return "настройки"
    elif exit_button.rect.collidepoint(pos):
        return "выход"
    elif back_button_settings.rect.collidepoint(pos):
        return "назад_настройки"
    
    return None

game_state = 'menu'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_option = handle_menu_click(event.pos)
            if clicked_option == "играть":
                game_state = "playing"
            elif clicked_option == "выход":
                running = False
            elif clicked_option == "настройки":
                game_state = "settings"
            elif clicked_option == "назад_настройки":
                game_state = "menu"
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        level1.play(screen)
    elif game_state == "settings":
        draw_settings()
    clock.tick(FPS)

pygame.quit()

