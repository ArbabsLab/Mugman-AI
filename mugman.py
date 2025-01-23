import pygame
import os

MUGMAN_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "mug1.png")))]
EVILCUP_IMGS = MUGMAN_IMGS = [pygame.transform2x(pygame.image.load(os.path.join("assets", "evilcup1.png")))]
WIN_WIDTH = 600
WIN_HEIGHT = 800

class Mugman:
    IMGS = MUGMAN_IMGS
    MAX_ROTATION = 0
    ROT_VEL = 25
    ANIMATION_TIME = 5

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        dp = self.vel*self.tick_count + 0.5 * 3 * self.tick_count**2

        if dp >= 16:
            dp = (dp/abs(dp)) * 16
        
        if dp < 0:
            dp -= 2
        
        self.y = self.y + dp

        if dp < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL