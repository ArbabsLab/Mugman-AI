import random
import pygame
import os

pygame.init()

MUGMAN_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "mug1.png")))]
EVILCUP_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "evilcup1.png")))]
WIN_WIDTH = 600
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

GAME_SPEED = 20
OBSTACLES = []

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
  
    GAP = 200
    VEL = 5

    def __init__(self, image):
        self.image = image
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIN_WIDTH
        self.rect.y = 325

    def update(self):
        self.rect.x -= GAME_SPEED
        if self.rect.x < -self.rect.width:
            OBSTACLES.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
