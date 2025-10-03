
import os
import sys
import math

if not __package__:
    __package__ = ((lambda p, d:
                    (".".join(p[-(n := p[::-1].index(d) + 1):]),
                    sys.path.insert(0, os.sep.join(p[:-n])))[0])(
                        os.path.realpath(__file__).split(os.sep)[:-1], "game"))

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

musc = pygame.mixer.music.load("game/assets/music/keys-of-moon-lonesome-journey.mp3")
music_volume = 1
pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.play(-1)



font_large = pygame.font.SysFont('Arial', 64)
font_small = pygame.font.SysFont('Arial', 32)


play_button = Button(250, 200, 300, 60, "Играть")
settings_button = Button(250, 300, 300, 60, "Настройки")
exit_button = Button(250, 400, 300, 60, "Выход")

back_button_settings = Button(40,75,100,60,"Назад")

def slider(sc, coor, len_, units, active_unit, mcoor, LKM):
    global peremennaya
    xm, ym = mcoor[0], mcoor[1]
    pygame.draw.line(sc, 'black', coor, (coor[0]+len_, coor[1]), 3)
    step = len_//units
    pygame.draw.circle(sc, 'red', (coor[0]+step*active_unit, coor[1]), 10)
    if LKM and math.hypot(xm - (coor[0]+step*active_unit), ym - coor[1]) <= 20:
        if (xm - coor[0])//step >= 1 and (xm - coor[0])//step <= units:
            peremennaya = (xm - coor[0])//step

def draw_menu():
    screen.fill(THEME) 
    
    title = font_large.render("Dead world", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    play_button.draw(screen=screen, font=font_small)
    settings_button.draw(screen=screen, font=font_small)
    exit_button.draw(screen=screen, font=font_small)
    
    screen.blit(title, title_rect)
    
    pygame.display.flip()

def draw_settings(xm, ym, LKM):
    screen.fill("#984141")
    
    title = font_large.render("Настройки", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    sound_set = font_small.render("Музыка", True, "#ffffff")
    sound_set_rect = sound_set.get_rect(center=(160, 200))
    
    back_button_settings.draw(screen=screen, font=font_small)
    
    screen.blit(title, title_rect)
    
    screen.blit(sound_set, sound_set_rect)
    
    slider(screen, [250,200], 200, 10, peremennaya, [xm,ym], LKM)
    
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
LKM = False
peremennaya = 0
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LKM = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                LKM = False
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        level1.play(screen)
    elif game_state == "settings":
        xm, ym = pygame.mouse.get_pos()
        draw_settings(xm, ym, LKM)
    clock.tick(FPS)

pygame.quit()

