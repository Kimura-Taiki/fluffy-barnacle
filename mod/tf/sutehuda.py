#                 20                  40                  60                 79
import pygame
from typing import Callable

from mod.const import WX, WY, screen, BLACK
from mod.huda import Huda
from mod.tf.taba_factory import TabaFactory

HAND_X_RATE: Callable[[int], float] = lambda i: 80-80*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2+70-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0.0

sutehuda_factory = TabaFactory(inject_kwargs={
    "draw": Huda.shadow_draw, "hover": Huda.detail_draw
}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
