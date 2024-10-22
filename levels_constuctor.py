import pygame
import sys
import os
import time
from tkinter import Tk, filedialog

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

start_image = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
start_image.fill(GREEN)
finish_image = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
finish_image.fill(RED)
def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            images[filename[:2]] = img  
    return images
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

    def clear(self):
        self.sprites.clear()
        self.start_set = False
        self.finish_set = False


    def add_sprite(self, x, y, image, designation):
        if 0 <= x < COLUMN_COUNT and 0 <= y < ROW_COUNT:
            existing_sprite = next((s for s in self.sprites if s.rect.topleft == (x * CELL_WIDTH, y * CELL_HEIGHT)), None)
            if existing_sprite:
                if existing_sprite.designation == "S" and designation != "S":
                    self.start_set = False
                if existing_sprite.designation == "F" and designation != "F":
                    self.finish_set = False
                self.sprites.remove(existing_sprite)
            
            if designation == "S":
                self.start_set = True
            elif designation == "F":
                self.finish_set = True

            new_sprite = Sprite(x, y, image, designation)
            self.sprites.append(new_sprite)

    def remove_sprite(self, pos):
        for sprite in self.sprites[:]:
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
        grid = [['..' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        for sprite in self.sprites:
            grid_x = sprite.rect.x // CELL_WIDTH
            grid_y = sprite.rect.y // CELL_HEIGHT
            if 0 <= grid_x < COLUMN_COUNT and 0 <= grid_y < ROW_COUNT:
                grid[grid_y][grid_x] = sprite.designation
        with open(filename, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')



    def show_save_warning(self):
        warning_surface = pygame.Surface((400, 200))
        warning_surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        message_lines = ["Файл не может быть", "сохранен, пока в нем", "нет старта и финиша"]
        y_offset = 40
        for line in message_lines:
            text_surface = font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(200, y_offset))
            warning_surface.blit(text_surface, text_rect)
            y_offset += 40
        warning_shown = True
        start_time = time.time()
        while warning_shown:
            screen.blit(warning_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
            pygame.display.flip()
            if time.time() - start_time > 3:
                warning_shown = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(30)

sprite_categories = {
    "Блоки": load_images_from_folder("Tile"),
    "Ловушки": load_images_from_folder("Trap"),
    "Враги": load_images_from_folder("Enemy"),
    "Начало/Конец": {"S": start_image, "F": finish_image}
}
level=Level()
def show_message_box(message):
    root = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Предупреждение")
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(50, 50, 300, 100)
    color = pygame.Color('lightskyblue3')
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True
        root.fill((30, 30, 30))
        txt_surface = font.render(message, True, color)
        root.blit(txt_surface, (input_box.x + 10, input_box.y + 30))
        pygame.draw.rect(root, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Level Builder")


def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        title_surface = font.render("Главное меню", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 4))
        font_buttons = pygame.font.Font(None, 56)
        edit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 75)
        new_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 75)
        pygame.draw.rect(screen, (0, 0, 255), edit_button)
        pygame.draw.rect(screen, (0, 0, 255), new_button)
        edit_text = font_buttons.render("Редактировать", True, WHITE)
        new_text = font_buttons.render("Создать новый", True, WHITE)
        screen.blit(edit_text, (edit_button.x + (edit_button.width - edit_text.get_width()) // 2, edit_button.y + (edit_button.height - edit_text.get_height()) // 2))
        screen.blit(new_text, (new_button.x + (new_button.width - new_text.get_width()) // 2, new_button.y + (new_button.height - new_text.get_height()) // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if edit_button.collidepoint(event.pos):
                    menu_running = False
                    load_level()
                elif new_button.collidepoint(event.pos):
                    menu_running = False
                    return


def load_level():
    root = Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Выберите файл уровня", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    root.destroy()

    if file_path:
        load_level_from_file(file_path)
    else:
        print("Файл не выбран")


def load_level_from_file(filename):
    try:
        with open(filename, 'r') as f:
            grid = [line.strip().split() for line in f.readlines()]
        level.clear() 
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != '..':  
                    if cell in sprite_categories["Начало/Конец"]:
                        image = sprite_categories["Начало/Конец"][cell]
                        level.add_sprite(x, y, image, cell)
                    else:
                        for category in sprite_categories:
                            if cell in sprite_categories[category]:
                                image = sprite_categories[category][cell]
                                level.add_sprite(x, y, image, cell)
    except FileNotFoundError:
        level.show_save_warning()




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
current_category = "Блоки"

main_menu()


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
                bg = pygame.image.load("Images/BG.png")
                bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

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
            if menu_visible:
                categories = list(sprite_categories.keys())
                for i, category in enumerate(categories):
                    category_rect = pygame.Rect(10, 60 + i * 40, 140, 30)
                    if category_rect.collidepoint(event.pos):
                        current_category = category
                        scroll_y = 0  
                        break

            selected_sprites = sprite_categories[current_category]
            for i, (designation, img) in enumerate(selected_sprites.items()):
                item_rect = pygame.Rect(160, 60 + i * (img.get_height() + 10) + scroll_y, img.get_width(), img.get_height())
                if item_rect.collidepoint(event.pos):
                    current_image = img
                    current_designation = designation

            if event.button == 1 and current_image is not None:
                pos = event.pos
                if not menu_visible or pos[0] > 160:  
                    grid_x = int(pos[0] // CELL_WIDTH)
                    grid_y = int(pos[1] // CELL_HEIGHT)
                    level.add_sprite(grid_x, grid_y, current_image, current_designation)
                    if keys[pygame.K_LSHIFT]:
                        dragging = True
            elif event.button == 3:  
                pos = event.pos
                if not menu_visible or pos[0] > 160: 
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
            "Ctrl + 1 - Установить старт",
            "Ctrl + 2 - Установить финиш"
        ]
        for i, instruction in enumerate(instructions):
            instruction_surface = font.render(instruction, True, WHITE)
            screen.blit(instruction_surface, (20, HEIGHT - 320 + 25 * i))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
