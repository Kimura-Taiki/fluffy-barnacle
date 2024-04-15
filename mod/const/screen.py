import pygame

FRAMES_PER_SECOND = 30
WX, WY = 1280, 720
pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

IMG_YATUBA_BG = pygame.image.load("pictures/yatuha_bg.png").convert_alpha()
