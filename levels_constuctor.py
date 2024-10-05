import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
GRID_SIZE = 50  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Builder")


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Sprite:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Level:
    def __init__(self):
        self.sprites = []

    def add_sprite(self, x, y, color):
        new_sprite = Sprite(x, y, color)
        self.sprites.append(new_sprite)

    def draw(self, surface):
        for sprite in self.sprites:
            sprite.draw(surface)

    def save_to_file(self, filename):
        grid = [['.' for _ in range(WIDTH // GRID_SIZE)] for _ in range(HEIGHT // GRID_SIZE)]
        for sprite in self.sprites:
            grid[sprite.rect.y // GRID_SIZE][sprite.rect.x // GRID_SIZE] = 'X' 
        with open(filename, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')


clock = pygame.time.Clock()
level = Level()
current_color = GREEN

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_color = GREEN
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = BLUE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                pos = event.pos
                grid_x = (pos[0] // GRID_SIZE) * GRID_SIZE
                grid_y = (pos[1] // GRID_SIZE) * GRID_SIZE
                level.add_sprite(grid_x, grid_y, current_color)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: 
                level.save_to_file("level.txt")

    screen.fill(WHITE)
    level.draw(screen)


    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

    font = pygame.font.Font(None, 36)
    text = font.render("Press 1: Green | Press 2: Red | Press 3: Blue | Press S: Save", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

