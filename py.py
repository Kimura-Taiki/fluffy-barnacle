import pygame
from typing import Callable

from mod.const import screen, clock, FRAMES_PER_SECOND, WX, WY, IMG_YATUBA_BG, UC_FLAIR, UC_DUST, UC_MAAI
from mod.controller import controller
from mod.timer_functions import start_timer, end_timer
from mod.banmen import Banmen

banmen = Banmen()

controller.get_hover = banmen.get_hover

img_taba = pygame.image.load("pictures/taba_selecter.png")

def mainloop() -> None:
    start_timer()

    controller.resolve_pygame_events()
    screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
    banmen.elpase()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
