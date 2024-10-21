import pygame
import sys
import os
import time

pygame.init()

WIDTH, HEIGHT = 1080, 720
ROW_COUNT = 19
COLUMN_COUNT = 32
CELL_WIDTH = WIDTH // COLUMN_COUNT
CELL_HEIGHT = HEIGHT // ROW_COUNT

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Level Builder")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

bg = pygame.image.load("Images/BG.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Создание изображений для старта и финиша в виде прямоугольников
start_image = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
start_image.fill(GREEN)
finish_image = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
finish_image.fill(RED)

def show_message_box(message):
    root = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Предупреждение")
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(50, 50, 300, 100)
    button_box = pygame.Rect(100, 150, 200, 40)
    color = pygame.Color('lightskyblue3')
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_box.collidepoint(event.pos):
                    done = True
        root.fill((30, 30, 30))
        txt_surface = font.render(message, True, color)
        root.blit(txt_surface, (input_box.x + 10, input_box.y + 30))
        pygame.draw.rect(root, color, input_box, 2)
        pygame.draw.rect(root, color, button_box)
        button_text = font.render("Закрыть предупреждение", True, (0, 0, 0))
        root.blit(button_text, (button_box.x + 10, button_box.y + 5))
        pygame.display.flip()
        clock.tick(30)
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Level Builder")

class Sprite:
    def __init__(self, x, y, image, designation):
        self.image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x * CELL_WIDTH, y * CELL_HEIGHT))
        self.designation = designation

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Level:
    def __init__(self):
        self.sprites = []
        self.start_set = False
        self.finish_set = False

    def add_sprite(self, x, y, image, designation):
        if designation == "S":
            self.start_set = True
        elif designation == "F":
            self.finish_set = True
        new_sprite = Sprite(x, y, image, designation)
        self.sprites.append(new_sprite)

    def remove_sprite(self, pos):
        for sprite in self.sprites[:]:  # Create a copy of the list for safe iteration
            if sprite.rect.collidepoint(pos):
                if sprite.designation == "S":
                    self.start_set = False
                elif sprite.designation == "F":
                    self.finish_set = False
                self.sprites.remove(sprite)
                break


    def draw(self, surface):
        for sprite in self.sprites:
            sprite.draw(surface)

    def save_to_file(self, filename):
        if not self.start_set or not self.finish_set:
            self.show_save_warning()
            return

        grid = [['.' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        for sprite in self.sprites:
            grid[sprite.rect.y // CELL_HEIGHT][sprite.rect.x // CELL_WIDTH] = sprite.designation
        with open(filename, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')

    def show_save_warning(self):
        warning_surface = pygame.Surface((400, 200))
        warning_surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        
        # Разделение текста на несколько строк и выравнивание по центру
        message_lines = [
            "Файл не может быть",
            "сохранен, пока в нем",
            "нет старта и финиша"
        ]
        
        y_offset = 40  # Расположение текста чуть выше
        for line in message_lines:
            text_surface = font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(200, y_offset))
            warning_surface.blit(text_surface, text_rect)
            y_offset += 40  # Смещение для следующей строки

        warning_shown = True
        start_time = time.time()
        while warning_shown:
            screen.blit(warning_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
            pygame.display.flip()

            # Проверка прошедшего времени
            if time.time() - start_time > 1.5:
                warning_shown = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(30)







    def clear(self):
        self.sprites.clear()
        self.start_set = False
        self.finish_set = False



def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            images[filename[:2]] = img  # Use first two digits of filename
    return images
clock = pygame.time.Clock()
level = Level()
images = load_images_from_folder("Tile")
current_image = None
current_designation = "00"
RUN = True
menu_visible = False
instructions_visible = True
scroll_y = 0
dragging = False

# Спрайты, разделенные на категории
sprite_categories = {
    "Блоки": load_images_from_folder("Tile"),
    "Ловушки": load_images_from_folder("Trap"),
    "Враги": load_images_from_folder("Enemy"),
    "Начало/Конец": {"S": start_image, "F": finish_image}
}


current_category = "Блоки"

def get_filename():
    root = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Enter filename")
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(50, 80, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = 'Введите название уровня'
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if text == 'Введите название уровня':
                            text = event.unicode
                        else:
                            text += event.unicode
        root.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        root.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(root, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Level Builder")
    return text


while RUN:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            if event.key == pygame.K_m:
                menu_visible = not menu_visible
            if event.key == pygame.K_i:
                instructions_visible = not instructions_visible
            if event.key == pygame.K_s:
                if not level.start_set or not level.finish_set:
                    level.show_save_warning()
                else:
                    filename = get_filename()
                    level.save_to_file(filename + ".txt")
            if event.key == pygame.K_ESCAPE:
                RUN = False
            if keys[pygame.K_LCTRL] and event.key == pygame.K_d:
                level.clear()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Обработка клика по кнопкам категорий
            if menu_visible:
                categories = list(sprite_categories.keys())
                for i, category in enumerate(categories):
                    category_rect = pygame.Rect(10, 60 + i * 40, 140, 30)
                    if category_rect.collidepoint(event.pos):
                        current_category = category
                        scroll_y = 0  # Сбросить прокрутку при смене категории
                        break

            selected_sprites = sprite_categories[current_category]
            for i, (designation, img) in enumerate(selected_sprites.items()):
                item_rect = pygame.Rect(160, 60 + i * (img.get_height() + 10) + scroll_y, img.get_width(), img.get_height())
                if item_rect.collidepoint(event.pos):
                    current_image = img
                    current_designation = designation

            if event.button == 1 and current_image is not None:
                pos = event.pos
                if not menu_visible or pos[0] > 160:  # Ensure click is outside menu area
                    grid_x = int(pos[0] // CELL_WIDTH)
                    grid_y = int(pos[1] // CELL_HEIGHT)
                    level.add_sprite(grid_x, grid_y, current_image, current_designation)
                    if keys[pygame.K_LSHIFT]:
                        dragging = True
            if event.button == 3:  # Удаление спрайта при правом клике
                pos = event.pos
                if not menu_visible or pos[0] > 160:  # Ensure click is outside menu area
                    level.remove_sprite(pos)


        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN and menu_visible and event.button == 4:
            scroll_y += 10
        elif event.type == pygame.MOUSEBUTTONDOWN and menu_visible and event.button == 5:
            scroll_y -= 10

    if dragging and current_image is not None:
        pos = pygame.mouse.get_pos()
        grid_x = int(pos[0] // CELL_WIDTH)
        grid_y = int(pos[1] // CELL_HEIGHT)
        level.add_sprite(grid_x, grid_y, current_image, current_designation)

    bg_resized = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg_resized, (0, 0))
    level.draw(screen)

    for x in range(0, WIDTH, CELL_WIDTH):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_HEIGHT):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

    menu_button_rect = pygame.Rect(WIDTH - 150, 10, 140, 40)
    pygame.draw.rect(screen, BLACK if not menu_visible else WHITE, menu_button_rect)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Menu (press M)", True, WHITE if not menu_visible else BLACK)
    screen.blit(button_text, (WIDTH - 140, 15))

    if menu_visible:
        categories = list(sprite_categories.keys())
        for i, category in enumerate(categories):
            category_rect = pygame.Rect(10, 60 + i * 40, 140, 30)
            pygame.draw.rect(screen, BLACK if current_category != category else WHITE, category_rect)
            category_text = font.render(category, True, WHITE if current_category != category else BLACK)
            screen.blit(category_text, (20, 65 + i * 40))

        selected_sprites = sprite_categories[current_category]
        for i, (designation, img) in enumerate(selected_sprites.items()):
            item_rect = pygame.Rect(160, 60 + i * (img.get_height() + 10) + scroll_y, img.get_width(), img.get_height())
            screen.blit(img, item_rect.topleft)
            text_surface = font.render(designation, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(item_rect.right + 10, item_rect.top))
            screen.blit(text_surface, text_rect)

    if instructions_visible:
        instructions_bg = pygame.Surface((620, 280))
        instructions_bg.fill(BLACK)
        screen.blit(instructions_bg, (10, HEIGHT - 330))
        instructions = [
            "Инструкция:",
            "M - Меню",
            "I - Скрыть/открыть инструкцию",
            "S - Сохранить",
            "Shift(удерж.) + ЛКМ - Заполнить соседние клетки",
            "Ctrl + D - Удалить все спрайты",
            "Right Click - Удалить спрайт",
        ]
        for i, instruction in enumerate(instructions):
            instruction_surface = font.render(instruction, True, WHITE)
            screen.blit(instruction_surface, (20, HEIGHT - 320 + 25 * i))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
