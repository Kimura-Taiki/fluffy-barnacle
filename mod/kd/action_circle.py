#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2

from mod.const import screen, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_YADOSI,\
    ACTION_CIRCLE_BASIC, ACTION_CIRCLE_ZENSIN, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    enforce
from mod.classes import Youso, popup_message, controller
from mod.mkt.utuwa import Utuwa

def mousedown(youso: Youso, mode: int=OBAL_KIHONDOUSA) -> None:
    if mode == OBAL_SYUUTYUU and youso.osame == 0:
        popup_message.add("集中力が0です")
        return
    controller.active = youso
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def _active(youso: Youso, mode: int=OBAL_KIHONDOUSA) -> None:
    # huda.detail_draw()
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        # controller.data_transfer = utuwa
        controller.active = None
    else:
        # source = {3: ACTION_CIRCLE_CARD, 2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
        source = {3: ACTION_CIRCLE_NEUTRAL, 2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
            int((diff_coord.angle_to([0, 0])+225)/90), ACTION_CIRCLE_ZENSIN)
        screen.blit(source=source, dest=controller.hold_coord-[250, 250])
