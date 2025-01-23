import random
import pygame
import os

pygame.init()

MUGMAN_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "mug1.png")))]
EVILCUP_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "evilcup1.png")))]
WIN_WIDTH = 600
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

class Mugman:
    IMGS = MUGMAN_IMGS
    X = 80
    Y = 310
    Y_DUCK = 340
    JUMP_VEL = 5

    def __init__(self):
        self.image = self.IMGs[0]
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
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X
        self.dino_rect.y = self.Y_DUCK
    
    def jump(self):
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.jump_state = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Evilcup():
  
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(EVILCUP_IMGS, False, True)
        self.PIPE_BOTTOM = EVILCUP_IMGS

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
       
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
      
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False