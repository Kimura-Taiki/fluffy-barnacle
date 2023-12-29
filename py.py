import pygame
from pygame.locals import QUIT
from pygame.surface import Surface
import sys
from typing import Callable

from mod.huda import Huda

WX, WY = 1280, 720
FRAMES_PER_SECOND = 30
CARDS = 6
DHX = 120
DA = -6.0
HAND_ANGLE = lambda i: -DA/2*(CARDS-1)+DA*i
HAND_X = lambda i: WX/2-DHX/2*(CARDS-1)+DHX*i
HAND_Y = lambda i: WY-60+abs(i*2-(CARDS-1))**2*2
AIHARA_KURO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (0, 0, 0))
UTURO: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_n_{i}.png").convert_alpha()

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()
hudas = [Huda(screen=screen, img=UTURO(i+1), angle=HAND_ANGLE(i), scale=0.6, x=HAND_X(i), y=HAND_Y(i)) for i in range(CARDS)]

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    on_huda = next((huda for huda in hudas[::-1] if huda.is_cursor_on()), None)
    if on_huda:
        screen.blit(source=AIHARA_KURO(str(on_huda.x), 36), dest=[0, 0])
        screen.blit(source=on_huda.img_nega, dest=[WX/2, 0])
    [huda.draw() for huda in hudas]
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
