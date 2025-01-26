import random
import pygame
import os

pygame.init()


SPRITESHEET = pygame.image.load(os.path.join("assets", "mugman_spritesheet.png"))

def extract_sprites(sheet, sprite_width, sprite_height, start_x=0, start_y=0, columns=1, rows=1, spacing_x=0, spacing_y=0):
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + col * (sprite_width + spacing_x)
            y = start_y + row * (sprite_height + spacing_y)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            frames.append(sprite)
    return frames

MUGMAN_RUN_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=10, start_y=50, columns=4, rows=1)



MUGMAN_JUMP_FRAMES = extract_sprites(SPRITESHEET, 32, 32, start_x=10, start_y=100, columns=1, rows=1)
MUGMAN_DUCK_FRAMES = extract_sprites(SPRITESHEET, 32, 32, start_x=10, start_y=150, columns=2, rows=1)

MUGMAN_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "mug1.png")))]

EVILCUP_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "evilcup1.png")))]
BG = pygame.image.load(os.path.join("assets", "game_track.png"))

WIN_WIDTH = 600
WIN_HEIGHT = 400
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))




class Mugman:
    IMGS = MUGMAN_IMGS
    X = 80
    Y = 310
    Y_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.image = self.IMGS[0]
        self.x = self.X
        self.y = self.Y

        #states
        self.run_state = True
        self.duck_state = False
        self.jump_state = False

        self.step_index = 0
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
        
        if self.step_index >= 10:
            self.step_index = 0
        
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
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y

    def duck(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y_DUCK
    
    def jump(self):
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
        self.rect.y = 200


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
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        WIN.blit(text, textRect)

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
        clock.tick(30)
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
        WIN.blit(MUGMAN_IMGS[0], (WIN_WIDTH // 2 - 20, WIN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)