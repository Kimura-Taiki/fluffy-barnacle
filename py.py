import pygame
from typing import Callable

from mod.const import UTURO, CARDS, screen, clock, FRAMES_PER_SECOND
from mod.tehuda import Tehuda
from mod.controller import controller

tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)])
controller.get_hover = tehuda.get_hover_huda

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
        screen.blit(source=MS_MINCHO_32PT(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}"),
            dest=[0, 0])
    return start_timer, end_timer
start_timer, end_timer = timer_functions()

def mainloop() -> None:
    start_timer()

    controller.resolve_pygame_events()
    screen.fill(color=(255, 255, 128))
    tehuda.elapse()
    controller.mouse_over()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
