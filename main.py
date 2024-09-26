import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen_width = 192 * 10 / 2
screen_height = 108 * 10 / 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Кнопка с эффектом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 162, 255)
BUTTON_PRESS_COLOR = (0, 100, 200)

img_sky = pygame.transform.scale(pygame.image.load("Images/sky.jpg"), (screen_width, screen_height))
img_space = pygame.transform.scale(pygame.image.load("Images/space.jpg"), (screen_width, screen_height))
img_options = pygame.transform.scale(pygame.image.load("Images/options.png"), (35, 35))

# Шрифт
font_small = pygame.font.Font(None, 36)

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect)
    label = font_small.render(text, True, WHITE)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))
def options_loop(running):
    button_rect = pygame.Rect(screen_width / 2 - 100, screen_height * 1 / 3 - 25, 200, 50)
    button_color = BUTTON_COLOR
    running = True
    while running:
        screen.blit(img_sky, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Кнопка Выход нажата!")
                    running = False
        if running == False:
            break

        # Проверка наведения мыши на кнопку
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            button_color = BUTTON_HOVER_COLOR
            if pygame.mouse.get_pressed()[0]:  # Проверка нажатия левой кнопки мыши
                button_color = BUTTON_PRESS_COLOR
        else:
            button_color = BUTTON_COLOR

        draw_button(button_rect, "Выход", button_color)

        pygame.display.flip()
    return running

def game_loop(running):
    # Простейшая игровая логика (например, просто изменение фона на черный)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Проверка нажатия на кнопку "Играть"
                if 0 < mouse_x < 35 and 0 < mouse_y < 35:
                    print("Открыты настройки")
                    running = options_loop(running)

        screen.fill(WHITE)
        screen.blit(img_options, (0, 0))
        pygame.display.flip()
    return running

def main():
    button_rect1 = pygame.Rect(screen_width / 2 - 100, screen_height * 1 / 3 - 25, 200, 50)
    button_rect2 = pygame.Rect(screen_width / 2 - 100, screen_height * 2 / 3 - 25, 200, 50)
    button_color1 = BUTTON_COLOR
    button_color2 = BUTTON_COLOR
    running = True
    while running:
        screen.blit(img_sky, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect1.collidepoint(event.pos):
                    print("Кнопка Играть нажата!")
                    running = game_loop(running)
                elif button_rect2.collidepoint(event.pos):
                    print("Кнопка Выход нажата!")
                    running = False
        if running == False:
            break

        # Проверка наведения мыши на кнопку
        if button_rect1.collidepoint(pygame.mouse.get_pos()):
            button_color1 = BUTTON_HOVER_COLOR
            if pygame.mouse.get_pressed()[0]:  # Проверка нажатия левой кнопки мыши
                button_color1 = BUTTON_PRESS_COLOR
        else:
            button_color1 = BUTTON_COLOR

        if button_rect2.collidepoint(pygame.mouse.get_pos()):
            button_color2 = BUTTON_HOVER_COLOR
            if pygame.mouse.get_pressed()[0]:  # Проверка нажатия левой кнопки мыши
                button_color2 = BUTTON_PRESS_COLOR
        else:
            button_color2 = BUTTON_COLOR

        draw_button(button_rect1, "Играть", button_color1)
        draw_button(button_rect2, "Выход", button_color2)

        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()
sys.exit()