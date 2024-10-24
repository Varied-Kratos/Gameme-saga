import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

with open("Levels/level_1.txt", "r") as l1:
    level_1 = [list(map(str, line.split())) for line in l1]
with open("Levels/level_2.txt", "r") as l2:
    level_2 = [list(map(str, line.split())) for line in l2]

map_width, map_height = 192 * 10, 108 * 10
screen_width, screen_height = 192 * 8, 108 * 8
button_width, button_height = 200, 100
tile_size = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gamem saga")

pygame.mixer.music.load("Sound/SeMe4iDzE-Gamem.mp3")

img_menu = pygame.transform.scale(pygame.image.load("images/menu.png"), (screen_width, screen_height))
img_bg = pygame.transform.scale(pygame.image.load("images/BG.png"), (screen_width, screen_height))


class Button:
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


class Spell:
    def __init__(self, x, y, direction, character):
        if character == "wizard":
            if direction == -1:
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("Wizard/Spell.png"), (tile_size, tile_size)), True, False)
            elif direction == 1:
                self.image = pygame.transform.scale(pygame.image.load("Wizard/Spell.png"), (tile_size, tile_size))
        elif character == "guard":
            if direction == -1:
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("Guard/Sword_swing.png"), (tile_size, tile_size)), True, False)
            elif direction == 1:
                self.image = pygame.transform.scale(pygame.image.load("Guard/Sword_swing.png"), (tile_size, tile_size))
        self.speed = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        self.counter = 0

    def collision(self):
        for tile in world.tile_list:
            if tile.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                return True
        return False

    def update(self, camera):
        self.counter += 1
        self.rect.x += self.speed * self.direction
        self.speed += 0.4

        for enemy in world.enemy_list:
            if enemy.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                enemy.alive = False
        screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))


class Player:
    def __init__(self, x, y, character):
        self.spells = []
        self.last_shot_time = 0
        self.shot_delay = 500
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
        self.direction = 1

    def update(self, camera, game_over, finish, pause, character):
        if not game_over and not pause:
            for spell in self.spells:
                if spell.counter < 100 and not spell.collision():
                    spell.update(camera)
                else:
                    self.spells.remove(spell)
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
            elif key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_k]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shot_delay:
                    if self.direction == -1:
                        spell = Spell(self.rect.x - tile_size, self.rect.centery - tile_size // 2, self.direction, character)
                        self.spells.append(spell)
                        self.last_shot_time = current_time
                    elif self.direction == 1:
                        spell = Spell(self.rect.x + tile_size, self.rect.centery - tile_size // 2, self.direction, character)
                        self.spells.append(spell)
                        self.last_shot_time = current_time
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
            if len(world.environment_list):
                if world.environment_list[1].rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    finish = True

            for enemy in world.enemy_list:
                if enemy.alive and enemy.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    game_over = True
            for trap in world.trap_list:
                if trap.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    game_over = True
            if self.rect.y > map_height:
                game_over = True

            self.rect.x += dx
            self.rect.y += dy

        else:
            self.image = pygame.transform.scale(pygame.image.load("images/Dead.png"), (tile_size * 2, tile_size * 2))
            if self.rect.y > map_height // 4:
                self.rect.y -= 5

        screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        camera[0], camera[1] = self.rect.x - screen_width // 2 + tile_size, self.rect.y - screen_height // 2
        return camera, game_over, finish, pause


class World:
    def __init__(self, data):
        global start_x, start_y
        self.tile_list = []
        self.enemy_list = []
        self.trap_list = []
        self.environment_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for something in row:
                try:
                    something = int(something)
                    if 10 <= something <= 24:
                        tile = Tile(col_count * tile_size, row_count * tile_size, something)
                        self.tile_list.append(tile)
                except ValueError:
                    if something == 'Tr':
                        trap = Trap(col_count * tile_size, row_count * tile_size)
                        self.trap_list.append(trap)
                    if something == 'Gh':
                        enemy = Enemy(col_count * tile_size, row_count * tile_size)
                        self.enemy_list.append(enemy)
                    if something == 'S' or something == 'F':
                        if something == 'S':
                            start_x, start_y = col_count * tile_size, row_count * tile_size
                        environment = Environment(col_count * tile_size, row_count * tile_size, something)
                        self.environment_list.append(environment)
                col_count += 1
            row_count += 1

    def draw(self, camera):
        visible_rect = pygame.Rect(camera[0], camera[1], screen_width, screen_height)
        for tile in self.tile_list:
            if tile.rect.colliderect(visible_rect):
                screen.blit(tile.image, tile.rect.move(-camera[0], -camera[1]))
        for enemy in self.enemy_list:
            if enemy.alive and enemy.rect.colliderect(visible_rect):
                enemy.update(camera)
        for trap in self.trap_list:
            if trap.rect.colliderect(visible_rect):
                screen.blit(trap.image, trap.rect.move(-camera[0], -camera[1]))
        for environment in self.environment_list:
            if environment.rect.colliderect(visible_rect):
                screen.blit(environment.image, environment.rect.move(-camera[0], -camera[1]))


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("Enemy/Ghost.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alive = True
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


class Trap:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("Trap/Trap.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tile:
    def __init__(self, x, y, number_of_tile):
        self.image = pygame.transform.scale(pygame.image.load(f"tile/{number_of_tile}.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Environment:
    def __init__(self, x, y, number_of_tile):
        if number_of_tile == 'S':
            self.image = pygame.image.load("Environment/Start.png")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        elif number_of_tile == 'F':
            self.image = pygame.image.load("Environment/Portal.png")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - tile_size


button_exit = Button(screen_width // 2 - button_width // 2, screen_height - button_height, "text_button")
button_start = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_continue = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_restart = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 3, "text_button")
button_wizard = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_guard = Button(screen_width // 2 - button_width // 2, screen_height - button_height, "text_button")
button_level1 = Button(screen_width // 2 - button_width // 2, screen_height - button_height * 2, "text_button")
button_level2 = Button(screen_width // 2 - button_width // 2, screen_height - button_height, "text_button")
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


def game_loop(running, character, level):
    global world
    world = World(level)
    player = Player(start_x, start_y, character)
    camera = [0, 0]
    game_over = False
    finish = False
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
                    for enemy in world.enemy_list:
                        enemy.alive = True
                    pygame.mixer.music.stop()
                    return running
                if button_options.rect.collidepoint(event.pos):
                    pause = True
                    wanna_restart = False
                    running, wanna_restart, pause = options(running, wanna_restart, pause)
                    if wanna_restart:
                        for enemy in world.enemy_list:
                            enemy.alive = True
                        pygame.mixer.music.stop()
                        return running
            elif event.type == pygame.KEYDOWN:
                if game_over and button_restart.rect.collidepoint(event.pos):
                    for enemy in world.enemy_list:
                        enemy.alive = True
                    pygame.mixer.music.stop()
                    return running
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    wanna_restart = False
                    running, wanna_restart, pause = options(running, wanna_restart, pause)
                    if wanna_restart:
                        for enemy in world.enemy_list:
                            enemy.alive = True
                        pygame.mixer.music.stop()
                        return running
        if game_over:
            pause = True
            button_restart.draw_button("Рестарт")

        camera, game_over, finish, pause = player.update(camera, game_over, finish, pause, character)

        if finish:
            for enemy in world.enemy_list:
                enemy.alive = True
            pygame.mixer.music.stop()
            return running

        button_options.draw_button("Настройки")

        pygame.display.update()
    return running


def choose_level(running, character):
    while running:
        screen.blit(img_menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_level1.rect.collidepoint(event.pos):
                    running = game_loop(running, character, level_1)
                elif button_level2.rect.collidepoint(event.pos):
                    running = game_loop(running, character, level_2)

        button_level1.draw_button("Уровень 1")
        button_level2.draw_button("Уровень 2")
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
                    running = choose_level(running, "wizard")
                elif button_guard.rect.collidepoint(event.pos):
                    running = choose_level(running,"guard")

        button_wizard.draw_button("Маг")
        button_guard.draw_button("Рыцарь")
        pygame.display.update()
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
        pygame.display.update()


if __name__ == "__main__":
    main()
pygame.quit()
