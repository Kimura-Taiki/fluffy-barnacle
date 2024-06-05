from pygame import Surface, Vector2 as V2, Rect
from typing import runtime_checkable, Protocol

from any.func import ratio_rect
from model.kard import Kard
from model.player import Player
from view.duel.duel_kard_open_square import DuelKardOpenSquare
from view.duel.duel_kard_slash_square import DuelKardSlashSquare
from view.duel.duel_icon_square import DuelIconSquare
from view.progress_helper import ProgressHelper

@runtime_checkable
class _Dq(Protocol):
    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        ...

@runtime_checkable
class _Dkq(Protocol):
    def __init__(
            self, rect: Rect, kard: Kard,
            canvas: Surface, seconds: float
        ) -> None:
        ...

_RATIO = V2(880, 475)
_SECONDS = 0.5

from ptc.transition import Transition
class DuelSlashTransition():
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

    def _dqs(self, p1: Player, p2: Player) -> tuple[
        _Dkq, _Dkq
    ]:
        ll = p1.hands[0].rank < p2.hands[0].rank
        rl = p1.hands[0].rank > p2.hands[0].rank
        li: list[tuple[type[_Dkq], tuple[int, int], Player, float]] = [
            (DuelKardSlashSquare if ll else DuelKardOpenSquare,
             (0, 0), p1, _SECONDS if ll else 0.0),
            (DuelKardSlashSquare if rl else DuelKardOpenSquare,
             (540, 0), p2, _SECONDS if rl else 0.0)
        ]
        dqs = [cls(
            rect=Rect(tpl, (340, 475)), kard=player.hands[0],
            canvas=self.canvas, seconds=f
        ) for cls, tpl, player, f in li]
        return (dqs[0], dqs[1])

    def _squares(self, p1: Player, p2: Player) -> list[_Dq]:
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=self.canvas, seconds=0.0)
        self.left_dq, self.right_dq = self._dqs(p1=p1, p2=p2)
        self.offset = V2(self.rect.topleft)
        return [q for q in [
            self.diq, self.left_dq, self.right_dq
        ] if isinstance(q, _Dq)]
