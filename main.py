import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

map_width, map_height = 192 * 10, 108 * 10
screen_width, screen_height = 192 * 8, 108 * 8
button_width, button_height = 200, 100

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gameme saga")

pygame.mixer.music.load("Sound/SeMe4iDzE-Gamem.mp3")

img_menu = pygame.transform.scale(pygame.image.load("images/menu.png"), (screen_width, screen_height))
img_bg = pygame.transform.scale(pygame.image.load("images/BG.png"), (screen_width, screen_height))

tile_size = 60


class Button():
    def __init__(self, x, y, button_type):
        self.button_type = button_type
        if button_type == "text_button":
            self.button = pygame.transform.scale(pygame.image.load("images/button.png"), (button_width, button_height))
        elif button_type == "options":
            self.button = pygame.transform.scale(pygame.image.load("images/options.png"), (100, 100))
        self.rect = self.button.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_button(self, text):
        screen.blit(self.button, (self.rect.x, self.rect.y))
        if self.button_type == "text_button":
            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


class Player():
    def __init__(self, x, y, character):
        self.on_ground = False
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            if character == "wizard":
                img_right_wizard = pygame.transform.scale(pygame.image.load(f'Wizard/Wizard1{num}.png'), (60, 105))
                img_left_wizard = pygame.transform.scale(pygame.image.load(f'Wizard/Wizard2{num}.png'), (60, 105))
                self.images_right.append(img_right_wizard)
                self.images_left.append(img_left_wizard)
            elif character == "guard":
                img_right_guard = pygame.transform.scale(pygame.image.load(f'Guard/Guard1{num}.png'), (60, 105))
                img_left_guard = pygame.transform.scale(pygame.image.load(f'Guard/Guard2{num}.png'), (60, 105))
                self.images_right.append(img_right_guard)
                self.images_left.append(img_left_guard)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, camera, game_over, pause):
        if not game_over and not pause:
            dx = 0
            dy = 0

            walk_cooldown = 5

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and self.on_ground:
                self.vel_y = -17
                self.jumped = True
                self.on_ground = False
            elif not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_d] and not key[pygame.K_a] or key[pygame.K_SPACE]:
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
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y > 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.on_ground = True

            for enemy in world.enemy_list:
                if enemy.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    game_over = True
            for trap in world.trap_list:
                if trap.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    game_over = True
            if self.rect.y > map_height:
                game_over = True

            self.rect.x += dx
            self.rect.y += dy

        else:
            self.image = pygame.image.load("Enemy/Ghost.png")
            if self.rect.y > map_height // 4:
                self.rect.y -= 5

        screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        camera[0], camera[1] = self.rect.x - screen_width // 2 + tile_size, self.rect.y - screen_height // 2
        return camera, pause, game_over


class World():
    def __init__(self, data):
        self.tile_list = []
        self.enemy_list = []
        self.trap_list = []
        self.environment_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for something in row:
                if 10 <= something <= 24:
                    tile = Tile(col_count * tile_size, row_count * tile_size, something)
                    self.tile_list.append(tile)
                if 40 <= something <= 49:
                    environment = Environment(col_count * tile_size, row_count * tile_size, something)
                    self.environment_list.append(environment)
                if something == 90:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    self.enemy_list.append(enemy)
                if something == 50:
                    trap = Trap(col_count * tile_size, row_count * tile_size)
                    self.trap_list.append(trap)
                col_count += 1
            row_count += 1

    def draw(self, camera):
        visible_rect = pygame.Rect(camera[0], camera[1], screen_width, screen_height)
        for tile in self.tile_list:
            if tile.rect.colliderect(visible_rect):
                screen.blit(tile.image, tile.rect.move(-camera[0], -camera[1]))
        for enemy in self.enemy_list:
            if enemy.rect.colliderect(visible_rect):
                enemy.update(camera)
        for trap in self.trap_list:
            if trap.rect.colliderect(visible_rect):
                screen.blit(trap.image, trap.rect.move(-camera[0], -camera[1]))
        for environment in self.environment_list:
            if environment.rect.colliderect(visible_rect):
                screen.blit(environment.image, environment.rect.move(-camera[0], -camera[1]))


class Enemy():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("Enemy/Ghost.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self, camera):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 60:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.move_direction == 1:
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        else:
            screen.blit(pygame.transform.flip(self.image, True, False),
                        (self.rect.x - camera[0], self.rect.y - camera[1]))


class Trap():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("Trap/Trap.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tile():
    def __init__(self, x, y, number_of_tile):
        self.image = pygame.transform.scale(pygame.image.load(f"tile/{number_of_tile}.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Environment():
    def __init__(self, x, y, number_of_tile):
        if number_of_tile == 40:
            self.image = pygame.transform.scale(pygame.image.load("Environment/Tree.png"), (180, 288))
            self.rect = self.image.get_rect()
            self.rect.x = x - self.image.get_size()[0] // 2 + tile_size
            self.rect.y = y - self.image.get_size()[1] + tile_size


level_1 = [
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 90, 99, 99, 50, 99, 99, 50, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99],
    [11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
     12, 12, 13],
]

world = World(level_1)

button_exit = Button(screen_width // 2 - button_width // 2, screen_height - button_height, "text_button")
button_start = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_continue = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_restart = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 3, "text_button")
button_wizard = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_guard = Button(screen_width // 2 - button_width // 2, screen_height - button_height, "text_button")
button_options = Button(0, 0, "options")


def options(running, wanna_restart, pause):
    while running and pause:
        screen.blit(img_menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.rect.collidepoint(event.pos):
                    running = False
                elif button_continue.rect.collidepoint(event.pos):
                    pause = False
                elif button_restart.rect.collidepoint(event.pos):
                    wanna_restart = True
                    return running, wanna_restart, pause
        button_continue.draw_button("Продолжить")
        button_exit.draw_button("Выход")
        button_restart.draw_button("Рестарт")
        pygame.display.update()
    return running, wanna_restart, pause


def game_loop(running, character):
    player = Player(tile_size * 4, map_height - tile_size, character)
    camera = [0, 0]
    game_over = False
    pause = False
    pygame.mixer.music.play(-1)
    while running:

        clock.tick(fps)

        screen.blit(img_bg, (0, 0))
        world.draw(camera)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and button_restart.rect.collidepoint(event.pos):
                    return running
                if button_options.rect.collidepoint(event.pos):
                    pause = True
                    wanna_restart = False
                    running, wanna_restart, pause = options(running, wanna_restart, pause)
                    if wanna_restart:
                        return running
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    wanna_restart = False
                    running, wanna_restart, pause = options(running, wanna_restart, pause)
                    if wanna_restart:
                        return running
        if game_over:
            pause = True
            button_restart.draw_button("Рестарт")

        camera, game_over, pause = player.update(camera, game_over, pause)

        button_options.draw_button("Настройки")

        pygame.display.update()
    return running


def choose_character(running):
    while running:
        screen.blit(img_menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_wizard.rect.collidepoint(event.pos):
                    running = game_loop(running, "wizard")
                elif button_guard.rect.collidepoint(event.pos):
                    running = game_loop(running,"guard")

        button_wizard.draw_button("Маг")
        button_guard.draw_button("Рыцарь")
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
                if button_start.rect.collidepoint(event.pos):
                    running = choose_character(running)
                elif button_exit.rect.collidepoint(event.pos):
                    running = False
        button_start.draw_button("Играть")
        button_exit.draw_button("Выход")
        pygame.display.flip()


if __name__ == "__main__":
    main()
pygame.quit()
