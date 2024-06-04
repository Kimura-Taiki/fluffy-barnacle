from pygame import Surface, Vector2 as V2, Rect
from typing import TypeVar, Generic

from any.func import ratio_rect
from any.screen import FRAMES_PER_SECOND
from any.timer_functions import frames
from model.player import Player
from model.ui_element import UIElement
from view.duel.duel_kard_open_square import DuelKardOpenSquare
from view.duel.duel_kard_slash_square import DuelKardSlashSquare
from view.duel.duel_icon_square import DuelIconSquare

_RATIO = V2(880, 475)
_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class DuelSlashTransition():
    def __init__(self, rect: Rect, p1: Player, p2: Player, canvas: Surface) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self._drawing_in_progress = True
        self.frames = frames()
        self.canvas = canvas
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=canvas, seconds=0.0)
        self.left_dq, self.right_dq = self.dqs(p1=p1, p2=p2)
        self.offset = V2(self.rect.topleft)
        self.squares: list[
            DuelIconSquare | DuelKardOpenSquare | DuelKardSlashSquare
        ] = [self.diq, self.left_dq, self.right_dq]
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

    def in_progress(self) -> bool:
        return self._drawing_in_progress

    def dqs(self, p1: Player, p2: Player) -> tuple[
        DuelKardOpenSquare | DuelKardSlashSquare,
        DuelKardOpenSquare | DuelKardSlashSquare
    ]:
        T = TypeVar('T')
        # T = Generic()
        ll = p1.hands[0].rank < p2.hands[0].rank
        rl = p1.hands[0].rank > p2.hands[0].rank
        li: list[T, tuple[tuple[int, int], Player, float]] = [
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

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT

    def _complete(self) -> None:
        self._drawing_in_progress = False
