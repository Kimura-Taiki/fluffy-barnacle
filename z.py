import pygame
from typing import Callable

from mod.const import screen, clock, FRAMES_PER_SECOND, WX, WY, IMG_YATUBA_BG, UC_FLAIR, UC_DUST, UC_MAAI, SIMOTE, UC_ZYOGAI
from mod.controller import controller
from mod.timer_functions import start_timer, end_timer
from mod.banmen import Banmen
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.ol.turns_progression.main_phase import MainPhase
from mod.ol.turns_progression.turns_progression import TurnProgression
from mod.ol.only_select_layer import OnlySelectLayer

banmen = Banmen()
banmen.send_ouka_to_ryouiki(hoyuusya=SIMOTE, from_mine=False, from_code=UC_MAAI, to_mine=True, to_code=UC_FLAIR, kazu=3)
banmen.send_ouka_to_ryouiki(hoyuusya=SIMOTE, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_FLAIR, kazu=3)
banmen.send_ouka_to_ryouiki(hoyuusya=SIMOTE, from_mine=False, from_code=UC_ZYOGAI, to_mine=False, to_code=UC_DUST, kazu=10)

moderator.delivery = banmen
moderator.append(TurnProgression(delivery=banmen, main_inject=banmen.inject_main_phase))
moderator.append(OnlySelectLayer(delivery=banmen, name="Hoge"))

controller.get_hover = lambda : moderator.get_hover() or banmen.get_hover()

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
