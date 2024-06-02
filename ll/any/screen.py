import pygame
from pygame import Vector2 as V2

FRAMES_PER_SECOND = 30
WX, WY = 1280, 720
WV2 = V2(WX, WY)
pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode(size=(WX, WY))
clock = pygame.time.Clock()
