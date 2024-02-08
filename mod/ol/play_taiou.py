#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import WX, WY, POP_TAIOUED
from mod.huda import Huda
from mod.moderator import moderator

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_UX: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_UY: Callable[[int, int], float] = lambda i, j: WY-150
SCALE_SIZE = 180

class PlayTaiou():
    name = "対応時にstat戻り値を与える為の空OverLayer"

    def __init__(self, huda: Huda) -> None:
        self.huda = huda
        self.delivery = huda.delivery
        self.inject_func = huda.delivery.inject_view

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.huda.card.kaiketu(delivery=self.huda.delivery, hoyuusya=self.huda.hoyuusya, huda=self.huda)
        moderator.pop()

    def close(self) -> Any:
        return POP_TAIOUED, self.huda

    def moderate(self, stat: int) -> None:
        ...

# compatible_with(, OverLayer)
