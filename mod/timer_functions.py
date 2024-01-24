import pygame
from typing import Callable

from mod.const import screen, LEMONCHIFFON, WX

def timer_functions() -> tuple[Callable[[], None], Callable[[], None]]:
    from time import time
    from mod.const import MS_MINCHO_32PT, FRAMES_PER_SECOND
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
        screen.blit(source=MS_MINCHO_32PT(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}"),
            dest=[WX-340, 240])
    return start_timer, end_timer
start_timer, end_timer = timer_functions()
