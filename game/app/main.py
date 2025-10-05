
import os
import sys
import math

if not __package__:
    __package__ = ((lambda p, d:
                    (".".join(p[-(n := p[::-1].index(d) + 1):]),
                    sys.path.insert(0, os.sep.join(p[:-n])))[0])(
                        os.path.realpath(__file__).split(os.sep)[:-1], "game"))

import pygame
from level1 import play
from ..components.Settings import draw_settings
from pygame_widgets.button import Button
import pygame_widgets

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
THEME = "#984141"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dead world")
clock = pygame.time.Clock()

def exit1():
    sys.exit()


font_large = pygame.font.SysFont('Arial', 64)
font_small = pygame.font.SysFont('Arial', 32)

play_button = Button(screen,250,200,300,60,text="Играть", font_size=32, inactiveColour="#5a2323", hoverColour="#ff7777",textColour="#ffffff", onClick=lambda: play(screen))
settings_button = Button(screen,250,300,300,60,text="Настройки", font_size=32, inactiveColour="#5a2323", hoverColour="#ff7777",textColour="#ffffff", onClick=lambda: draw_settings(screen))
exit_button = Button(screen,250,400,300,60,text="Выход", font_size=32, inactiveColour="#5a2323", hoverColour="#ff7777",textColour="#ffffff", onClick=lambda: exit1())

game_state = 'menu'
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    screen.fill(THEME) 
    
    title = font_large.render("Dead world", True, "#ffffff")
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    screen.blit(title, title_rect)
    clock.tick(FPS)
    pygame_widgets.update(events)

    pygame.display.flip()

pygame.quit()

