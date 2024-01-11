import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import sys
from typing import Callable
import time

from mod.const import UTURO, CARDS, screen, clock, FRAMES_PER_SECOND, MS_MINCHO
from mod.huda import Huda
from mod.taba import Taba
from mod.tehuda import Tehuda

class Mouse():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Huda | None = None
        self.get_hovered: Callable[[], Huda | None] = self._not_implemented_get_hovered
        self.active: Huda | None = None
    
    @staticmethod
    def _not_implemented_get_hovered() -> None:
        raise NotImplementedError("Mouse.get_hoveredが未定義です")

tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)])
mouse = Mouse()
mouse.get_hovered = tehuda.get_hovered_huda
times = [1.0]*FRAMES_PER_SECOND

def mainloop() -> None:
    start_time = time.time()  # 一周期の開始時刻を記録

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == 
    screen.fill(color=(255, 255, 128))
    tehuda.elapse()
    if (hovered_huda := mouse.get_hovered()):
        hovered_huda.hovered()

    end_time = time.time()  # 一周期の終了時刻を記録
    elapsed_time = end_time - start_time
    times.append(elapsed_time)
    times.pop(0)
    screen.blit(source=MS_MINCHO(f"One loop time: {round(elapsed_time*1000, 3):.3f} ms", 32), dest=[0, 120])
    screen.blit(source=MS_MINCHO(f"Frame time: {(sum(times)/FRAMES_PER_SECOND*1000):.3f} ms", 32), dest=[0, 160])
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
