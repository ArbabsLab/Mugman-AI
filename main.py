import math
import random
import pygame
import os
import neat
import pickle

pygame.init()

SPRITESHEET = pygame.image.load(os.path.join("assets", "mugman_spritesheet.png"))


def extract_sprites(sheet, sprite_width, sprite_height, start_x=0, start_y=0, columns=1, rows=1, spacing_x=0, spacing_y=0):
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + col * (sprite_width + spacing_x) + 1
            y = start_y + row * (sprite_height + spacing_y)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            sprite = pygame.transform.scale2x(sprite)
            frames.append(sprite)
    return frames


def extract_ops(sheet, sprite_width, sprite_height, start_x=0, start_y=0, columns=1, rows=1, spacing_x=0, spacing_y=0):
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + col * (sprite_width + spacing_x) + 1
            y = start_y + row * (sprite_height + spacing_y)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            sprite = pygame.transform.flip(sprite, 1, 0)
            sprite = pygame.transform.scale2x(sprite)
            frames.append(sprite)
    return frames


MUGMAN_RUN_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=25, start_y=10, columns=3, rows=1)
MUGMAN_JUMP_FRAMES = extract_sprites(SPRITESHEET, 32, 24, start_x=33, start_y=35, columns=1, rows=1)
MUGMAN_DUCK_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=220, start_y=10, columns=1, rows=1)

EVILCUP_IMGS = extract_ops(SPRITESHEET, 32, 32, start_x=0, start_y=220, columns=1, rows=1)
BG = pygame.image.load(os.path.join("assets", "game_track.png"))

WIN_WIDTH = 600
WIN_HEIGHT = 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def remove(index):
    player.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)


class Mugman:
    X = 80
    Y = 360
    Y_DUCK = 365
    JUMP_VEL = 6

    def __init__(self):
        self.run_img = MUGMAN_RUN_FRAMES
        self.duck_img = MUGMAN_DUCK_FRAMES
        self.jump_img = MUGMAN_JUMP_FRAMES

        self.image = self.run_img[0]
        self.x = self.X
        self.y = self.Y

        self.run_state = True
        self.duck_state = False
        self.jump_state = False

        self.frame_index = 0
        self.jump_vel = self.JUMP_VEL
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y

    def update(self, userInput):
        if self.run_state:
            self.run()
        if self.duck_state:
            self.duck()
        if self.jump_state:
            self.jump()

        if self.frame_index >= len(self.run_img):
            self.frame_index = 0

    def run(self):
        self.image = self.run_img[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.frame_index += 1

    def duck(self):
        self.image = self.duck_img[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y_DUCK

    def jump(self):
        self.image = self.jump_img[0]
        if self.jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.jump_state = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


class Evilcup:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rect.y = 325

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)



class Groundcup(Evilcup):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 325


class Flycup(Evilcup):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 300


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, player, ge, nets
    run = True
    clock = pygame.time.Clock()

    obstacles = []
    player = []
    ge = []
    nets = []

    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)

    for genome_id, genome in genomes:
        player.append(Mugman())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        WIN.blit(text, (WIN_WIDTH // 2, 40))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        WIN.blit(BG, (x_pos_bg, y_pos_bg))
        WIN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            WIN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WIN.fill((255, 255, 255))
        background()

        for i, mugman in enumerate(player):
            mugman.draw(WIN)
            mugman.update(pygame.key.get_pressed())

        if len(player) == 0:
            break

        if len(obstacles) == 0:
            ob = 0

            if ob == 0:
                obstacles.append(Groundcup(EVILCUP_IMGS[0]))
            else:
                obstacles.append(Flycup(EVILCUP_IMGS[0]))

        for obby in obstacles:
            obby.draw(WIN)
            obby.update()
            for i, mugman in enumerate(player):
                if mugman.rect.colliderect(obby.rect):
                    ge[i].fitness -= 1
                    remove(i)

        for i, mugman in enumerate(player):
            output = nets[i].activate((mugman.rect.y, distance((mugman.rect.x, mugman.rect.y), obby.rect.midtop)))
            if output[0] > 0.5 and mugman.rect.y == Mugman.Y:
                mugman.jump_state = True
                mugman.run_state = False

        score()
        background()
        clock.tick(10)
        pygame.display.update()


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
