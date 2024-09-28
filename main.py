import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

button_width, button_height = 200, 100
map_width, map_height = 192 * 10, 108 * 10
screen_width, screen_height = 192 * 5, 108 * 5

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gameme saga")

img_menu = pygame.transform.scale(pygame.image.load("images/menu.png"), (screen_width, screen_height))
img_button = pygame.transform.scale(pygame.image.load("images/button.png"), (button_width, button_height))
img_options = pygame.transform.scale(pygame.image.load("images/exit.png"), (100, 100))
img_bg = pygame.transform.scale(pygame.image.load("images/BG.png"), (screen_width, screen_height))


button_start = pygame.Rect(screen_width / 2 - button_width / 2, screen_height - button_height * 2, button_width,
                           button_height)
button_finish = pygame.Rect(screen_width / 2 - button_width / 2, screen_height - button_height, button_width,
                            button_height)
button_options = pygame.Rect(100, 100, 100, 100)

title_size = 12 * 5

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.transform.scale(pygame.image.load(f'Guard/Guard1{num}.png'), (60, 105))
            img_left = pygame.transform.scale(pygame.image.load(f'Guard/Guard2{num}.png'), (60, 105))
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
    def update(self, camera):
        dx = 0
        dy = 0

        walk_cooldown = 5

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -17
            self.jumped = True
        elif key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False or key[pygame.K_SPACE]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0



        self.rect.x += dx
        self.rect.y += dy

        screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        camera[0], camera[1] = self.rect.x - screen_width // 2 + 60, self.rect.y - screen_height // 2
        return camera
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class World():
    def __init__(self, data):
        self.tile_list = []

        img_block1 = pygame.transform.scale(pygame.image.load("images/Block1.png"), (title_size, title_size))
        img_grass1 = pygame.transform.scale(pygame.image.load("images/Grass1.png"), (title_size, title_size))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 2:
                    img_rect = img_block1.get_rect()
                    img_rect.x = col_count * title_size
                    img_rect.y = row_count * title_size
                    tile = [img_block1, img_rect]
                    self.tile_list.append(tile)
                if tile == 3:
                    img_rect = img_grass1.get_rect()
                    img_rect.x = col_count * title_size
                    img_rect.y = row_count * title_size
                    tile = [img_grass1, img_rect]
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    def draw(self, camera):

        visible_rect = pygame.Rect(camera[0], camera[1], screen_width, screen_height)

        # Рисуем только видимые тайлы
        for tile in self.tile_list:
            if tile[1].colliderect(visible_rect):
                screen.blit(tile[0], tile[1].move(-camera[0], -camera[1]))

        #for tile in self.tile_list:
            #screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
world_data = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 3],
    [3, 0, 3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3],
    [3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

player = Player(title_size, title_size)
world = World(world_data)

def draw_button(rect, text, color):
    screen.blit(img_button, (rect.x, rect.y))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def options(running):
    running = False
    return running
def game_loop(running):
    camera = [0, 0]
    while running:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 0 < mouse_x < 100 and 0 < mouse_y < 100:
                    print("Выход")
                    running = options(running)

        screen.blit(img_bg, (0, 0))

        world.draw(camera)

        camera = player.update(camera)

        screen.blit(img_options, (0, 0))
        pygame.display.flip()
    return running
def main():
    running = True
    while running:
        screen.blit(img_menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    print("Кнопка Играть нажата!")
                    running = game_loop(running)
                elif button_finish.collidepoint(event.pos):
                    print("Кнопка Выход нажата!")
                    running = False
        draw_button(button_start, "Играть", (0, 0, 0))
        draw_button(button_finish, "Выход", (0, 0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
pygame.quit()
