import pygame
from time import time
from typing import Callable

from any.func import rect_fill
from any.font import MS_MINCHO_COL
from any.screen import screen, WX, FRAMES_PER_SECOND

_FONT_SIZE = 36

def timer_functions() -> tuple[Callable[[], None], Callable[[], None]]:
    from time import time
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
        rect_fill(color="lemonchiffon", rect=[WX-340, 240, WX, 40])
        # pygame.draw.rect(surface=screen, color="lemonchiffon", rect=[WX-340, 240, WX, 40], width=0)
        screen.blit(source=MS_MINCHO_COL(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}", _FONT_SIZE, "black"),
            dest=[WX-340, 240])
    return start_timer, end_timer
start_timer, end_timer = timer_functions()
