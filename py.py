import pygame
from pygame.locals import QUIT
import sys

from mod.huda import Huda

WX = 800
WY = 600
FRAMES_PER_SECOND = 30

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

def uturo(i: int) -> pygame.surface.Surface:
    return pygame.image.load(f"cards/na_00_hajimari_a_n_{i}.png").convert_alpha()
hudas = [Huda(screen=screen, img=uturo(1), angle=6.0, scale=0.6, x=340, y=540),
         Huda(screen=screen, img=uturo(2), angle=0.0, scale=0.6, x=400, y=540),
         Huda(screen=screen, img=uturo(3), angle=-6.0, scale=0.6, x=460, y=540),
         ]

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    [huda.draw() for huda in hudas]
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
