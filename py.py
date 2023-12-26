import pygame
from pygame.locals import QUIT
import sys

WX = 800
WY = 600
FRAMES_PER_SECOND = 30

img = pygame.image.load("cards/na_00_hajimari_a_n_1.png")   # 340x475

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    screen.blit(source=img, dest=[100, 100])
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
