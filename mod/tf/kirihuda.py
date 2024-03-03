#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, KIRIHUDA_CIRCLE_NEUTRAL, KIRIHUDA_CIRCLE_CARD, USAGE_USED, IMG_USED, SIMOTE, OBAL_USE_CARD
# from mod.classes import Callable, Card, Huda, moderator, popup_message, controller
from mod.classes import Callable, Huda, moderator, controller
from mod.tf.taba_factory import TabaFactory
# from mod.ol.others_basic_action import obal_func
from mod.ol.standard_action_layer import use_card_layer

HAND_X_RATE: Callable[[int], float] = lambda i: 600/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-144
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0

def _draw(huda: Huda) -> None:
    if huda.usage == USAGE_USED:
        huda.shadow_draw()
        screen.blit(source=pygame.transform.rotate(surface=IMG_USED, angle=0.0 if huda.hoyuusya == SIMOTE else 180.0), dest=huda.dest-[100, 100])
    elif not huda.card.is_full(delivery=huda.delivery, hoyuusya=huda.hoyuusya):
        huda.shadow_draw()
    else:
        huda.available_draw()

def _mousedown(huda: Huda) -> None:
    controller.active = huda
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def _active(huda: Huda) -> None:
    huda.detail_draw()
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=KIRIHUDA_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        controller.data_transfer = huda
    else:
        if int((diff_coord.angle_to([0, 0])+225)/90) == 3:
            screen.blit(source=KIRIHUDA_CIRCLE_CARD, dest=controller.hold_coord-[250, 250])
        else:
            screen.blit(source=KIRIHUDA_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])

# _use_card: Callable[[Card], Callable[[Huda], None]] = lambda card: obal_func(cards=[card], text=f"切り札から「{card.name}」カードを使います", mode=OBAL_USE_CARD)

def _mouseup(huda: Huda) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50 or int((diff_coord.angle_to([0, 0])+225)/90) != 3:
        return
    # _use_card(huda.card)(huda)
#                 20                  40                  60                 79
    moderator.append(use_card_layer(cards=[huda.card], name=f"切り札から「{\
        huda.card.name}」を使います", youso=huda, mode=OBAL_USE_CARD))
    

kirihuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active, "mouseup": _mouseup
    # "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active, "mouseup": _mouseup
}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
