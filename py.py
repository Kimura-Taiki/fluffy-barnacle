import pygame
from pygame.locals import QUIT
import sys

from mod.const import *
from mod.huda import Huda
from mod.taba import Taba
from mod.tehuda import Tehuda

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()
taba = Tehuda.made_by_files(screen=screen, strs=[UTURO(i) for i in range(1, CARDS+1)])

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    on_huda = next((huda for huda in taba[::-1] if huda.is_cursor_on()), None)
    if on_huda:
        screen.blit(source=AIHARA_KURO(str(on_huda.x), 36), dest=[0, 0])
        screen.blit(source=on_huda.img_nega, dest=[WX/2, 0])
    [huda.draw() for huda in taba]
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
