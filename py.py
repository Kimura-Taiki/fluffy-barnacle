import pygame
from typing import Callable

from mod.const import screen, clock, FRAMES_PER_SECOND, WX, WY, IMG_YATUBA_BG, UC_FLAIR, UC_DUST, UC_MAAI
from mod.controller import controller
from mod.timer_functions import start_timer, end_timer
from mod.banmen import Banmen
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.ol.main_phase import MainPhase

banmen = Banmen()

moderator.delivery = banmen
moderator.append(MainPhase(inject_func=banmen.inject_main_phase))

# controller.get_hover = banmen.get_hover
controller.get_hover = lambda : moderator.get_hover() if moderator.get_hover() else banmen.get_hover()

img_taba = pygame.image.load("pictures/taba_selecter.png")

def mainloop() -> None:
    start_timer()

    controller.resolve_pygame_events()
    screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
    banmen.elpase()
    moderator.elapse()
    popup_message.elapse()
    popup_message.draw()

    end_timer()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
