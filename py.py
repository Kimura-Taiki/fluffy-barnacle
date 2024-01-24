import pygame
from typing import Callable

from mod.const import UTURO, HONOKA, CARDS, screen, clock, FRAMES_PER_SECOND, LEMONCHIFFON, BLACK, WX, WY, IMG_YATUBA_BG \
    , IMG_MAAI_AREA, IMG_DUST_AREA
from mod.controller import controller
from mod.youso import Youso
from mod.mikoto import Mikoto
from mod.utuwa import Utuwa
from mod.timer_functions import start_timer, end_timer


own_mikoto = Mikoto(is_own=True)
enemy_mikoto = Mikoto(is_own=False)
# maai = Utuwa(img=IMG_MAAI_AREA, is_own=True, num=10, x=)

def get_hover() -> Youso | None:
    if y1 := own_mikoto.get_hover():
        return y1
    else:
        return enemy_mikoto.get_hover()
controller.get_hover = get_hover

img_taba = pygame.image.load("pictures/taba_selecter.png")

def mainloop() -> None:
    start_timer()

    controller.resolve_pygame_events()
    screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
    own_mikoto.elapse()
    enemy_mikoto.elapse()
    screen.blit(source=IMG_MAAI_AREA, dest=[540, 330])
    screen.blit(source=IMG_DUST_AREA, dest=[680, 330])
    controller.mouse_over()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
