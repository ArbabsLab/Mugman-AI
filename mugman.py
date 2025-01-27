import random
import pygame
import os

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




class Mugman:
    X = 80
    Y = 360
    Y_DUCK = 365
    JUMP_VEL = 8.5

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
        
        if userInput[pygame.K_UP] and not self.jump_state:
            self.run_state = False
            self.duck_state = False
            self.jump_state = True
        elif userInput[pygame.K_DOWN] and not self.jump_state:
            self.run_state = False
            self.duck_state = True
            self.jump_state = False
        elif not (self.jump_state or userInput[pygame.K_DOWN]):
            self.run_state = True
            self.duck_state = False
            self.jump_state = False


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
        if self.jump_vel < - self.JUMP_VEL:
            self.jump_state = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Evilcup():
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH
        self.rect.y = 325

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


def main():

    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Mugman()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        WIN.blit(text, (500, 40))

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

        userInput = pygame.key.get_pressed()

        player.draw(WIN)
        player.update(userInput)

        if len(obstacles) == 0:
            ob = random.randint(0, 1)

            if ob == 0:
                obstacles.append(Groundcup(EVILCUP_IMGS[0]))
            else:
                obstacles.append(Flycup(EVILCUP_IMGS[0]))
        
        for obby in obstacles:
            obby.draw(WIN)
            obby.update()
            if player.rect.colliderect(obby.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
        
        

        score()
        clock.tick(10)
        pygame.display.update()



def menu(death_count):
    global points
    run = True
    while run:
        WIN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)
            WIN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        WIN.blit(text, textRect)
        WIN.blit(MUGMAN_RUN_FRAMES[0], (WIN_WIDTH // 2 - 20, WIN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)