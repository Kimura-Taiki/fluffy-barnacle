import pygame
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, AIHARA_KURO
from mod.huda import Huda
from mod.taba import Taba

HAND_X_RATE = 120
HAND_ANGLE_RATE = -6.0
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE/2*(j-1)+HAND_ANGLE_RATE*i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE/2*(j-1)+HAND_X_RATE*i
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+abs(i*2-(j-1))**2*2

class Tehuda(Taba):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__(data)
        self.held_on: Huda | None = None

    def get_hovered_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)

    def elapse(self) -> None:
        [huda.draw() for huda in self]

    @classmethod
    def made_by_files(cls, surfaces: list[Surface]) -> "Tehuda":
        j = len(surfaces)
        return Tehuda(data=[Huda(img=v, angle=HAND_ANGLE(i, j), scale=0.6, x=HAND_X(i, j), y=HAND_Y(i, j),
                                 hovered=cls._hovered_tehuda)
                            for i, v in enumerate(surfaces)])

    @staticmethod
    def _hovered_tehuda(huda: Huda) -> None:
        screen.blit(source=AIHARA_KURO(str(huda.x), 36), dest=[0, 0])
        screen.blit(source=huda.img_nega, dest=[WX-huda.img_nega.get_width(), 0])
