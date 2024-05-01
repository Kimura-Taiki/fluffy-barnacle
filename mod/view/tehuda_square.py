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

class TehudaSquare():
    def __init__(self, cards: list[Card], rect: Rect, is_reverse: bool = False) -> None:
        self.cards = cards
        self.rect = rect
        mag = rect.width/600 if rect.height*600 > rect.width*240 else rect.height/240
        j = len(cards)
        self.hudas = [Huda(
            img=card.zh.img,
            mid=V2(rect.centerx*2-HAND_X_MAG(rect, i, j, mag), rect.centery*2-HAND_Y_MAG(rect, i, j, mag))
                if is_reverse else V2(HAND_X_MAG(rect, i, j, mag), HAND_Y_MAG(rect, i, j, mag)),
            angle=HAND_ANGLE(i, j)+(180.0 if is_reverse else 0.0),
            scale=0.6*mag,
            draw=_draw,
            hover=_hover)
            for i, card in enumerate(cards)]

    def get_hover(self) -> Element | None:
        return next((huda for huda in self.hudas[::-1] if huda.is_cursor_on()), None)

    def draw(self) -> None:
        rect_fill(color=(255, 0, 0, 128), rect=self.rect)
        for huda in self.hudas:
            huda.draw()

def _draw(huda: Huda) -> None:
    rad = radians(-huda.angle-90.0)
    dest = huda.dest+V2(cos(rad), sin(rad))*(40.0*huda.scale/0.6 if huda == router.get_hover() else 0.0)
    screen.blit(source=huda.img, dest=dest)

def _hover(huda: Huda) -> None:
    screen.blit(source=huda.img_hover, dest=(0, 0))
