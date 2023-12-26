import pygame
from pygame.locals import QUIT
import sys

WX = 800
WY = 600
FRAMES_PER_SECOND = 30

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()