from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect
from model.player import Player
from view.duel.duel_icon_square import DuelIconSquare
from view.duel.duel_kard_open_square import DuelKardOpenSquare
from view.progress_helper import ProgressHelper

_RATIO = V2(880, 475)
_SECONDS = 0.5

from ptc.transition import Transition
class DuelOpenTransition():
    def __init__(self, rect: Rect, p1: Player, p2: Player, canvas: Surface) -> None:
        self._ratio, self.in_progress, _, _, self.get_hover, self.elapse\
            = ProgressHelper(seconds=_SECONDS).provide_progress_funcs()
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.squares = self._squares(p1=p1, p2=p2)

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        for square in self.squares:
            square.offset_draw(offset=self.offset)

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

    def _squares(self, p1: Player, p2: Player) -> list[DuelIconSquare | DuelKardOpenSquare]:
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=self.canvas, seconds=0.0)
        self.left_dkoq, self.right_dkoq = self.dkoqs(p1=p1, p2=p2)
        self.offset = V2(self.rect.topleft)
        return [self.diq, self.left_dkoq, self.right_dkoq]
