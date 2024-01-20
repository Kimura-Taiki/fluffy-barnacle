import pygame
from typing import Callable

from mod.const import UTURO, HONOKA, CARDS, screen, clock, FRAMES_PER_SECOND, LEMONCHIFFON, BLACK, WX, WY
from mod.tehuda import Tehuda
from mod.controller import controller
from mod.youso import Youso
from mod.gottenon import Gottenon
from mod.gottena import Gottena
from mod.mikoto import Mikoto


# own_tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)], is_own=True)
# gottena = Gottena(data=[Gottenon(text="山札", x=WX-140, y=WY-210), Gottenon(text="手札", x=WX-140, y=WY-150),
#                         Gottenon(text="伏せ札・捨て札", x=WX-140, y=WY-90), Gottenon(text="切り札", x=WX-140, y=WY-30)])
own_mikoto = Mikoto(is_own=True)
enemy_tehuda = Tehuda.made_by_files(surfaces=[HONOKA(i) for i in range(1, CARDS+1)], is_own=False)
def get_hover() -> Youso | None:
    # if youso := gottena.get_hover_gotten():
    if youso := own_mikoto.gottena.get_hover_gotten():
        return youso
    # elif youso := own_tehuda.get_hover_huda():
    # elif youso := own_mikoto.tehuda.get_hover_huda():
    elif youso := own_mikoto.view_taba.get_hover_huda():
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
    screen.fill(color=LEMONCHIFFON)
    screen.blit(source=pygame.transform.rotate(surface=img_taba, angle=180), dest=[0, 0])
    # own_tehuda.elapse()
    # own_mikoto.tehuda.elapse()
    own_mikoto.view_taba.elapse()
    enemy_tehuda.elapse()
    # gottena.elapse()
    own_mikoto.gottena.elapse()
    controller.mouse_over()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
