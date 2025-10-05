import pygame

class Button:
    def __init__(self, x, y, width, height, text, color="#5a2323"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self,screen,font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            highlight_color = "#9e3b3b" 
        else:
            highlight_color = self.color
            
        pygame.draw.rect(screen, highlight_color, self.rect)
        pygame.draw.rect(screen, "#000000", self.rect, 3) 
        
        text_surface = font.render(self.text, True, "#ffffff")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)