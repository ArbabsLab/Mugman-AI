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