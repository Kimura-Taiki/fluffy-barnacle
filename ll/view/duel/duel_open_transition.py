from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect, make_progress_funcs
from any.timer_functions import make_ratio_func
from model.player import Player
from model.ui_element import UIElement
from view.duel.duel_icon_square import DuelIconSquare
from view.duel.duel_kard_open_square import DuelKardOpenSquare

_RATIO = V2(880, 475)
_SECONDS = 0.5

from ptc.transition import Transition
class DuelOpenTransition():
    def __init__(self, rect: Rect, p1: Player, p2: Player, canvas: Surface) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=_SECONDS)
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=canvas, seconds=0.0)
        self.left_dkoq, self.right_dkoq = self.dkoqs(p1=p1, p2=p2)
        self.offset = V2(self.rect.topleft)
        self.squares: list[DuelIconSquare | DuelKardOpenSquare] = [self.diq, self.left_dkoq, self.right_dkoq]
        self.ui_element = UIElement(mousedown=self._complete)

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def draw(self) -> None:
        for square in self.squares:
            square.offset_draw(offset=self.offset)

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def dkoqs(self, p1: Player, p2: Player) -> tuple[DuelKardOpenSquare, DuelKardOpenSquare]:
        li: list[tuple[tuple[int, int], Player, float]] = [
            ((0, 0), p1, _SECONDS if p1.hands[0].rank < p2.hands[0].rank else 0.0),
            ((540, 0), p2, _SECONDS if p1.hands[0].rank > p2.hands[0].rank else 0.0)
        ]
        dkoqs = [DuelKardOpenSquare(
            rect=Rect(tpl, (340, 475)), kard=player.hands[0],
            canvas=self.canvas, seconds=f
        ) for tpl, player, f in li]
        return (dkoqs[0], dkoqs[1])
