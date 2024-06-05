from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect
from model.player import Player
from view.duel.duel_kard_move_square import DuelKardMoveSquare
from view.duel.duel_icon_square import DuelIconSquare
from view.progress_helper import ProgressHelper

_RATIO = V2(880, 475)
_SECONDS = 0.5

from ptc.transition import Transition
class DuelEngageTransition():
    def __init__(self, rect: Rect, p1: Player, p2: Player, canvas: Surface) -> None:
        _, self.in_progress, _, _, self.get_hover, self.elapse\
            = ProgressHelper(seconds=_SECONDS).provide_progress_funcs()
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.diq = DuelIconSquare(rect=Rect(300, 95, 280, 280), canvas=canvas, seconds=_SECONDS)
        li: list[tuple[tuple[int, int], Player, bool]] = [((0, 0), p1, True), ((540, 0), p2, False)]
        self.left_dkoq, self.right_dkoq = [DuelKardMoveSquare(
            rect=Rect(tpl, (340, 475)), kard=player.hands[0],
            is_left=is_left, canvas=canvas, seconds=_SECONDS
        ) for tpl, player, is_left in li]
        self.offset = V2(self.rect.topleft)
        self.squares: list[DuelIconSquare | DuelKardMoveSquare] = [self.diq, self.left_dkoq, self.right_dkoq]

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        for square in self.squares:
            square.offset_draw(offset=self.offset)
