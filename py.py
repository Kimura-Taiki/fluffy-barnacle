import pygame
from pygame.locals import QUIT
import sys

from mod.const import UTURO, CARDS, screen, clock, FRAMES_PER_SECOND
from mod.huda import Huda
from mod.taba import Taba
from mod.tehuda import Tehuda

tehuda = Tehuda.made_by_files(strs=[UTURO(i) for i in range(1, CARDS+1)])
clicked = False
target = None
class Mouse():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Huda | None = None

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    tehuda.elapse()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
