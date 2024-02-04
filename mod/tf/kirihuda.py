#                 20                  40                  60                 79
import pygame
from typing import Callable

from mod.const import WX, WY, screen, BRIGHT
from mod.huda import Huda, available_draw
from mod.controller import controller
from mod.tf.taba_factory import TabaFactory

HAND_X_RATE: Callable[[int], float] = lambda i: 600/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-144

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    else:
        available_draw(huda=huda)
    return None

kirihuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw
}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
