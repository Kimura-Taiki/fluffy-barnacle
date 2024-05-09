from pygame import Rect, Vector2 as V2, Surface
from typing import Callable
from math import sin, cos, radians

# Squareプロトコルを満たす
from ptc.square import Square

from mod.card import Card
from mod.view.huda import Huda
from ptc.element import Element
from mod.const.screen import screen
from mod.router import router
from mod.const.func import rect_fill
from mod.view.crb import Crb

MARGIN = 2

class CrbSquare():
    def __init__(self, rect: Rect, is_reverse: bool = False) -> None:
        self.rect = rect
        self.crbs = [Crb(Surface((16, 16)), Rect(rect.left+MARGIN, rect.top+rect.height*i/4+MARGIN,
                                                 rect.width-MARGIN*2, rect.height/4-MARGIN*2), 1.0)
                     for i in range(4)]

    def get_hover(self) -> Element | None:
        return next((crb for crb in self.crbs if crb.is_cursor_on()), None)

    def draw(self) -> None:
        rect_fill(color=(255, 255, 0, 128), rect=self.rect)
        for crb in self.crbs:
            crb.draw()
