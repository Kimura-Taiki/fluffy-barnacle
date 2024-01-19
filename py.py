import pygame
from typing import Callable

from mod.const import UTURO, HONOKA, CARDS, screen, clock, FRAMES_PER_SECOND, LEMONCHIFFON, BLACK, WX, WY
from mod.tehuda import Tehuda
from mod.controller import controller
from mod.youso import Youso
from mod.gottenon import Gottenon

gottenon = Gottenon(text="手札", x=WX/2, y=WY/2)
own_tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)], is_own=True)
enemy_tehuda = Tehuda.made_by_files(surfaces=[HONOKA(i) for i in range(1, CARDS+1)], is_own=False)
def get_hover() -> Youso | None:
    if youso := own_tehuda.get_hover_huda():
        return youso
    else:
        return enemy_tehuda.get_hover_huda()
controller.get_hover = get_hover

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
        pygame.draw.rect(surface=screen, color=LEMONCHIFFON, rect=[0, 240, 340, 40], width=0)
        screen.blit(source=MS_MINCHO_32PT(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}"),
            dest=[0, 240])
    return start_timer, end_timer
start_timer, end_timer = timer_functions()

img_taba = pygame.image.load("pictures/taba_selecter.png")

def mainloop() -> None:
    start_timer()

    controller.resolve_pygame_events()
    pygame.draw.rect(surface=screen, color=LEMONCHIFFON, rect=[0, 0, WX-340, WY], width=0)
    pygame.draw.rect(surface=screen, color=BLACK, rect=[WX-340, 0, 340, WY], width=0)
    pygame.draw.rect(surface=screen, color=BLACK, rect=[0, 0, 340, WY], width=0)
    screen.blit(source=img_taba, dest=[WX-340, 480])
    screen.blit(source=pygame.transform.rotate(surface=img_taba, angle=180), dest=[0, 0])
    own_tehuda.elapse()
    enemy_tehuda.elapse()
    gottenon.draw()
    controller.mouse_over()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
