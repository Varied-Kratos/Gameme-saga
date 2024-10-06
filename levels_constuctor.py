import pygame
import sys
import os

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


bg = pygame.image.load("Images/BG.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

class Sprite:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x * CELL_WIDTH, y * CELL_HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Level:
    def __init__(self):
        self.sprites = []

    def add_sprite(self, x, y, image):
        new_sprite = Sprite(x, y, image)
        self.sprites.append(new_sprite)

    def remove_sprite(self, pos):
        for sprite in self.sprites:
            if sprite.rect.collidepoint(pos):
                self.sprites.remove(sprite)
                break

    def draw(self, surface):
        for sprite in self.sprites:
            sprite.draw(surface)

    def save_to_file(self, filename):
        grid = [['.' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        for sprite in self.sprites:
            grid[sprite.rect.y // CELL_HEIGHT][sprite.rect.x // CELL_WIDTH] = 'X'
        with open(filename, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')

def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            images[filename] = img
    return images

clock = pygame.time.Clock()
level = Level()
images = load_images_from_folder("Tile") 
current_image = None

RUN = True
menu_visible = False  
scroll_y = 0  

while RUN:
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
            
            if event.key == pygame.K_ESCAPE:
                RUN = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and current_image is not None:  
                pos = event.pos
                grid_x = int(pos[0] // CELL_WIDTH)
                grid_y = int(pos[1] // CELL_HEIGHT)
                level.add_sprite(grid_x, grid_y, current_image)
            elif event.button == 3:  
                level.remove_sprite(event.pos)

            
            if menu_visible:
                for i, (name, img) in enumerate(images.items()):
                    item_rect = pygame.Rect(10, 60 + i * (img.get_height() + 10) + scroll_y, img.get_width(), img.get_height())
                    if item_rect.collidepoint(event.pos):
                        current_image = img

        
        if event.type == pygame.MOUSEBUTTONDOWN and menu_visible and event.button == 4:  
            scroll_y += 10
        elif event.type == pygame.MOUSEBUTTONDOWN and menu_visible and event.button == 5:  
            scroll_y -= 10

    
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
        for i, (name, img) in enumerate(images.items()):
            item_rect = pygame.Rect(10, 60 + i * (img.get_height() + 10) + scroll_y, img.get_width(), img.get_height())
            screen.blit(img, item_rect.topleft)

            
            text_surface = font.render(name, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(item_rect.right + 10, item_rect.top))
            screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
