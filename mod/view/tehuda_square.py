from pygame import Rect, Vector2 as V2
from typing import Callable
from mod.card import Card
from mod.view.huda import Huda

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[Rect, int, int], float] = lambda r, i, j: r.centerx-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[Rect, int, int], float] = lambda r, i, j: r.bottom-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class TehudaSquare():
    def __init__(self, cards: list[Card], rect: Rect, is_reverse: bool = False) -> None:
        self.cards = cards
        self.rect = rect
        j = len(cards)
        self.hudas = [Huda(
            img=card.zh.img,
            mid=V2(rect.centerx*2-HAND_X(rect, i, j), rect.centery*2-HAND_Y(rect, i, j))
                if is_reverse else V2(HAND_X(rect, i, j), HAND_Y(rect, i, j)),
            angle=HAND_ANGLE(i, j)+(180.0 if is_reverse else 0.0),
            scale=0.6)
            for i, card in enumerate(cards)]

    def draw(self) -> None:
        for huda in self.hudas:
            huda.draw()
