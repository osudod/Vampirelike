
import pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра с главным меню")
clock = pygame.time.Clock()

# Шрифты
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

# Создаем объекты меню
play_button = Button(250, 200, 300, 60, "Играть")
settings_button = Button(250, 300, 300, 60, "Настройки")
exit_button = Button(250, 400, 300, 60, "Выход")

# Функция для отрисовки главного меню
def draw_menu():
    screen.fill((50, 50, 50))  # Серый фон
    
    title = font_large.render("Игра", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    
    # Рисуем элементы меню
    play_button.draw()
    settings_button.draw()
    exit_button.draw()
    
    # Выравниваем текст заголовка по центру
    screen.blit(title, title_rect)
    
    pygame.display.flip()

# Функция для обработки кликов на кнопках
def handle_menu_click(pos):
    if play_button.rect.collidepoint(pos):
        return "играть"
    elif settings_button.rect.collidepoint(pos):
        return "настройки"
    elif exit_button.rect.collidepoint(pos):
        return "выход"
    
    return None

game_state = 'menu'
# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Обработка кликов мыши в меню
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_option = handle_menu_click(event.pos)
            if clicked_option == "играть":
                print("Запускаем игру...")
                # Здесь можно перейти к игровому состоянию (раскомментировать строку ниже)
                game_state = "playing"
                
            elif clicked_option == "выход":
                running = False
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
            screen.fill((0, 0, 0))
            pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

# Для полноценного меню нужно добавить:
# 1. Обработку нажатия клавиш (например, ESC для выхода)
# 2. Звуковые эффекты при кликах
# 3. Анимации или другие визуальные эффекты

class MainMenu:
    def __init__(self):
        self.buttons = [
            Button(250, 200, 300, 60, "Играть", GRAY),
            Button(250, 300, 300, 60, "Настройки", GRAY),
            Button(250, 400, 300, 60, "Выход", GRAY)
        ]

    def draw(self):
        screen.fill((50, 50, 50))  # Серый фон
        title = font_large.render("Игра", True, WHITE)
        
        for button in self.buttons:
            mouse_pos = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_pos):
                highlight_color = (200, 200, 200)  # Светлый оттенок
            else:
                highlight_color = GRAY
                
            pygame.draw.rect(screen, highlight_color, button.rect)
            pygame.draw.rect(screen, BLACK, button.rect, 3)  # Граница
            
        for i, button in enumerate(self.buttons):
            text_surface = font_small.render(button.text, True, WHITE)
            text_rect = text_surface.get_rect(center=button.rect.center)
            screen.blit(text_surface, text_rect)

        title_rect = title.get_rect(midtop=(SCREEN_WIDTH//2, 50))
        # Привязка к верхнему краю экрана
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//2 - len(title)*10, 40, len(title)*10 + 20, 30), 2)
        
        screen.blit(title, title_rect)

# Для продвинутого меню:
#  - Добавить анимации
#  - Реализовать подменю (например для настроек)
#  - Использовать медиафайлы: изображения логотипа, звуки
