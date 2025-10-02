import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра с главным меню")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont('Arial', 64)
font_small = pygame.font.SysFont('Arial', 32)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self):
        # Рисуем кнопку с подсветкой при наведении
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            highlight_color = (200, 200, 200)  # Светлый оттенок
        else:
            highlight_color = GRAY
            
        pygame.draw.rect(screen, highlight_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)  # Граница
        
        # Рисуем текст кнопки
        text_surface = font_small.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)