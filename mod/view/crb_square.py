from pygame import Rect, Vector2 as V2
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

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[Rect, int, int], float] = lambda r, i, j: r.centerx-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i
HAND_X_MAG: Callable[[Rect, int, int, float], float] = lambda r, i, j, f: r.centerx+(-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i)*f

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[Rect, int, int], float] = lambda r, i, j: r.bottom-60+HAND_Y_DIFF(i, j)**2*2
HAND_Y_MAG: Callable[[Rect, int, int, float], float] = lambda r, i, j, f: r.bottom+(-60+HAND_Y_DIFF(i, j)**2*2)*f

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class CrbSquare():
    def __init__(self, rect: Rect, is_reverse: bool = False) -> None:
        self.rect = rect
        mag = rect.width/280 if rect.height*280 > rect.width*240 else rect.height/240

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        rect_fill(color=(255, 255, 0, 128), rect=self.rect)
