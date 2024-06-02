from pygame import Rect, Surface, SRCALPHA, transform, Color, Vector2 as V2
from typing import Any
from copy import deepcopy

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color, cursor_in_rect
from any.font import MS_MINCHO_COL
from model.player import Player, OBSERVER
from model.ui_element import UIElement
from view.log_square import LogSquare
from ptc.bridge import Bridge

from pygame import Color
def _blend_colors(c1: Color, c2: Color, t: float=0.5) -> Color:
    """
    2つの色の中間色を計算する関数。
    
    :param a: 最初の色 (pygame.Color)
    :param b: 2番目の色 (pygame.Color)
    :param t: 補間パラメータ (0.0から1.0の範囲)
    :return: 中間色 (pygame.Color)
    """
    if not (0.0 <= t <= 1.0):
        raise ValueError("補間パラメータtは0.0から1.0の範囲でなければなりません。")
    
    r = c1.r + (c2.r - c1.r) * t
    g = c1.g + (c2.g - c1.g) * t
    b = c1.b + (c2.b - c1.b) * t
    a = c1.a + (c2.a - c1.a) * t
    
    return Color(int(r), int(g), int(b), int(a))

from ptc.square import Square
class PlayerSquare():
    _RATIO = (320, 288)
    _LOG_RATIO = (136, 190)

    def __init__(self, player: Player, rect: Rect, bridge: Bridge) -> None:
        self.player = player
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        self.view_params = (0, 0)
        self.img = self._img()
        self.log_squares = self._log_squares()
        self.ui_element = UIElement()

    def get_hover(self) -> UIElement | None:
        return self.ui_element if cursor_in_rect(rect=self.rect) else None

    def draw(self) -> None:
        if self._view_params() != self.view_params:
            self.view_params = self._view_params()
            self.img = self._img()
            self.log_squares = self._log_squares()
        screen.blit(source=self.img, dest=self.rect)
        for log_square in self.log_squares:
            log_square.draw()

    def elapse(self) -> None:
        for lq in self.log_squares:
            lq.elapse()

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        hand_name = "empty" if len(self.player.hands) == 0 else self.player.hands[0].name
        rect_fill(color=self._color(), rect=Rect((0, 0), self._RATIO), surface=img)
        img.blit(source=MS_MINCHO_COL(f"{self.player.name} ({hand_name})", 24, "black"), dest=(0, 0))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
    
    def _color(self) -> Color:
        tc = translucented_color(self.player.color)
        bc = Color("black")
        return tc if self.player.alive else _blend_colors(tc, bc, 0.8)

    def _log_squares(self) -> list[LogSquare]:
        return [LogSquare(
            kard=kard,
            rect=Rect((10+i*80, 70), self._LOG_RATIO),
            canvas=self.img
        ) for i, kard in enumerate(self.player.log)]

    def _view_params(self) -> tuple[Any, ...]:
        return (deepcopy(self.player.log), deepcopy(self.player.hands), self.player.alive)

    @property
    def _now_player(self) -> Player:
        return next((player for player in self.bridge.board.players if player.name == self.player.name), OBSERVER)

    @classmethod
    def search_by_player(cls, squares: list[Square], player: Player) -> 'PlayerSquare':
        if ps := next((
            square for square in squares if
            isinstance(square, PlayerSquare) and
            square.player.name == player.name
        ), None):
            return ps
        else:
            raise ValueError(
                f"該当プレイヤーはいません\nplayer = {player}"
            )

    @classmethod
    def search_v2_by_player(cls, squares: list[Square], player: Player) -> V2:
        return V2(cls.search_by_player(squares=squares, player=player).rect.center)
