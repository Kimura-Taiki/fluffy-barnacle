from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect
from any.screen import FRAMES_PER_SECOND
from any.timer_functions import frames
from model.player import Player
from model.ui_element import UIElement
from view.duel_kard_move_square import DuelKardMoveSquare
from view.duel_icon_square import DuelIconSquare

_RATIO = V2(880, 475)
_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class DuelEngageTransition():
    def __init__(self, rect: Rect, p1: Player, p2: Player, canvas: Surface) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self._drawing_in_progress = True
        self.frames = frames()
        self.canvas = canvas
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=canvas, seconds=_SECONDS)
        li: list[tuple[tuple[int, int], Player, bool]] = [((0, 0), p1, True), ((540, 0), p2, False)]
        self.left_dkoq, self.right_dkoq = [DuelKardMoveSquare(
            rect=Rect(tpl, (340, 475)), kard=player.hands[0],
            is_left=is_left, canvas=canvas, seconds=_SECONDS
        ) for tpl, player, is_left in li]
        self.offset = V2(self.rect.topleft)
        self.squares: list[DuelIconSquare | DuelKardMoveSquare] = [self.diq, self.left_dkoq, self.right_dkoq]
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

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT

    def _complete(self) -> None:
        self._drawing_in_progress = False
