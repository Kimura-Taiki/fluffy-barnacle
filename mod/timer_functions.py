import pygame
from typing import Callable

from mod.const import screen, LEMONCHIFFON, WX

def timer_functions() -> tuple[Callable[[], None], Callable[[], None]]:
    from time import time
    from mod.const import FRAMES_PER_SECOND, MS_MINCHO_COL, FONT_SIZE_TIMER, BLACK
    log = 0.0
    times = [0.01]*FRAMES_PER_SECOND
    def start_timer() -> None:
        nonlocal log
        log = time()
    def end_timer() -> None:
        nonlocal log, times
        elapsed_time = time()-log
        times.append(elapsed_time)
        times.pop(0)
        pygame.draw.rect(surface=screen, color=LEMONCHIFFON, rect=[WX-340, 240, WX, 40], width=0)
        screen.blit(source=MS_MINCHO_COL(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}", FONT_SIZE_TIMER, BLACK),
            dest=[WX-340, 240])
    return start_timer, end_timer
start_timer, end_timer = timer_functions()
