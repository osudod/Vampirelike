
import os
import sys
import math

import pygame
from menu import play
from Settings import draw_settings
from Buttons import Button

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

def handle_menu_click(pos):
    if play_button.rect.collidepoint(pos):
        return "играть"
    elif settings_button.rect.collidepoint(pos):
        return "настройки"
    elif exit_button.rect.collidepoint(pos):
        return "выход"

game_state = 'menu'
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_option = handle_menu_click(event.pos)
            if clicked_option == "играть":
                game_state = "playing"
            elif clicked_option == "выход":
                running = False
            elif clicked_option == "настройки":
                game_state = "settings"
    screen.fill(THEME) 
    
    title = font_large.render("Dead world", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    play_button.draw(screen,font_small)
    settings_button.draw(screen,font_small)
    exit_button.draw(screen,font_small)
    
    screen.blit(title, title_rect)
    clock.tick(FPS)

    pygame.display.flip()
    
    if game_state == "playing":
        play(screen)
        game_state = "menu"
    elif game_state == "settings":
        draw_settings(screen)
        game_state = "menu"

pygame.quit()

