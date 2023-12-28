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
hudas = [Huda(screen=screen, img=uturo(i+1), angle=6.0-6.0*i, scale=0.6, x=340+60*i, y=540) for i in range(3)]

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    on_huda = next((huda for huda in hudas[::-1] if huda.is_cursor_on()), None)
    if on_huda:
        font = pygame.font.Font("Aiharahudemojikaisho_free305.ttf", 36)
        text = font.render(str(on_huda.x), True, (0, 0, 0))
        screen.blit(source=text, dest=[0, 0])
    [huda.draw() for huda in hudas]
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
