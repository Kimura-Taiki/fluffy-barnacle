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

huda = Huda(screen=screen, img=pygame.image.load("cards/na_00_hajimari_a_n_1.png").convert_alpha(),
            angle=75.0, scale=0.4, x=100, y=100)
font = pygame.font.Font("Aiharahudemojikaisho_free305.ttf", size=36)
text = font.render("とぅるー！", True, (0, 0, 0))

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    huda.draw()
    if huda.is_cursor_on():
        screen.blit(source=text, dest=[300, 300])
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
