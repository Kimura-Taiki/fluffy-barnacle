import pygame
from pygame.locals import QUIT
import sys
from typing import Callable

from mod.const import UTURO, CARDS, screen, clock, FRAMES_PER_SECOND
from mod.huda import Huda
from mod.taba import Taba
from mod.tehuda import Tehuda

class Mouse():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Huda | None = None
        self.get_hovered: Callable[[], Huda | None] = self._not_implemented_get_hovered
    
    @staticmethod
    def _not_implemented_get_hovered() -> None:
        raise NotImplementedError("Mouse.get_hoveredが未定義です")

tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)])
mouse = Mouse()
mouse.get_hovered = tehuda.get_hovered_huda

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    tehuda.elapse()
    mouse.hovered = mouse.get_hovered()
    if mouse.hovered:
        mouse.hovered.hovered()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
