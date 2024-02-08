#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, KIRIHUDA_CIRCLE_NEUTRAL, KIRIHUDA_CIRCLE_CARD
from mod.huda import Huda
from mod.controller import controller
from mod.tf.taba_factory import TabaFactory
from mod.popup_message import popup_message

HAND_X_RATE: Callable[[int], float] = lambda i: 600/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-144

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    else:
        huda.available_draw()
    return None

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

def _mouseup(huda: Huda) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50 or int((diff_coord.angle_to([0, 0])+225)/90) != 3:
        return
    _use_card(huda=huda)

def _use_card(huda: Huda) -> None:
    if not huda.can_play():
        # popup_message.add(text="カードの使用条件を満たしていません")
        return
    popup_message.add(text=f"手札から「{huda.card.name}」を使います")
    huda.play()

kirihuda_factory = TabaFactory(inject_kwargs={
    "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active
}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
