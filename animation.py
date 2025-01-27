import random
import pygame
import os
import neat

pygame.init()

SPRITESHEET = pygame.image.load(os.path.join("assets", "mugman_spritesheet.png"))
BG = pygame.image.load(os.path.join("assets", "game_track.png"))

def extract_sprites(sheet, sprite_width, sprite_height, start_x=0, start_y=0, columns=1, rows=1, spacing_x=0, spacing_y=0, flip=False):
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + col * (sprite_width + spacing_x)
            y = start_y + row * (sprite_height + spacing_y)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            if flip:
                sprite = pygame.transform.flip(sprite, True, False)
            sprite = pygame.transform.scale2x(sprite)
            frames.append(sprite)
    return frames

MUGMAN_RUN_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=25, start_y=10, columns=3, rows=1)
MUGMAN_JUMP_FRAMES = extract_sprites(SPRITESHEET, 32, 24, start_x=33, start_y=35, columns=1, rows=1)
MUGMAN_DUCK_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=220, start_y=10, columns=1, rows=1)
EVILCUP_IMGS = extract_sprites(SPRITESHEET, 32, 32, start_x=0, start_y=220, columns=1, rows=1)

WIN_WIDTH, WIN_HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

class Mugman:
    X, Y, Y_DUCK, JUMP_VEL = 80, 360, 365, 8.5

    def __init__(self):
        self.run_img = MUGMAN_RUN_FRAMES
        self.duck_img = MUGMAN_DUCK_FRAMES
        self.jump_img = MUGMAN_JUMP_FRAMES
        self.image = self.run_img[0]
        self.x, self.y = self.X, self.Y
        self.run_state, self.duck_state, self.jump_state = True, False, False
        self.frame_index, self.jump_vel = 0, self.JUMP_VEL
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.X, self.Y

    def update(self, action):
        if action == 0 and not self.jump_state:
            self.run_state, self.duck_state, self.jump_state = False, False, True
        elif action == 1 and not self.jump_state:
            self.run_state, self.duck_state, self.jump_state = False, True, False
        elif action == 2:
            self.run_state, self.duck_state, self.jump_state = True, False, False

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
        self.rect.x, self.rect.y = self.X, self.Y
        self.frame_index += 1

    def duck(self):
        self.image = self.duck_img[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.X, self.Y_DUCK

    def jump(self):
        self.image = self.jump_img[0]
        if self.jump_state:
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
        self.rect.x, self.rect.y = WIN_WIDTH, 325

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

class Groundcup(Evilcup):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 325

class Flycup(Evilcup):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 300

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    nets = []
    players = []
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Mugman())
        genome.fitness = 0
        ge.append(genome)

    clock = pygame.time.Clock()
    run = True
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []

    while run and len(players) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for i, player in enumerate(players):
            inputs = [player.rect.y, obstacles[0].rect.x - player.rect.x] if obstacles else [player.rect.y, WIN_WIDTH]
            output = nets[i].activate(inputs)
            action = output.index(max(output))
            player.update(action)

            if len(obstacles) > 0 and player.rect.colliderect(obstacles[0].rect):
                ge[i].fitness -= 1
                players.pop(i)
                nets.pop(i)
                ge.pop(i)

        WIN.fill((255, 255, 255))
        for player in players:
            player.draw(WIN)
        pygame.display.update()
        clock.tick(10)

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
