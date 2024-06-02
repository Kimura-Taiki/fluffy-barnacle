from pygame import Rect
from copy import deepcopy
from copy import copy

from any.func import enforce, rect_fill, translucented_color
from any.screen import screen, WX, WY
from any.pictures import IMG_BG
from model.player import Player, OBSERVER
from model.ui_element import UIElement
from ptc.bridge import Bridge
from ptc.square import Square
from view.board_view import BoardView
from view.player_square import PlayerSquare

# from ptc.view import View
from ptc.transition import Transition
class PlayerSelectView:
    def __init__(self, bridge: Bridge, exclude: Player=OBSERVER) -> None:
        self.bridge = bridge
        self.exclude = exclude
        self.board_view = enforce(bridge.view, BoardView)
        self.player_squares = self._player_squares()
        self.other_squares = self._other_squares()

    def rearrange(self) -> None:
        """レイアウトの再配置を行います"""
        ...

    def get_hover(self) -> UIElement | None:
        """ホバー中の要素を取得します"""
        for square in self.player_squares:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        """ボードを描画します"""
        screen.blit(source=IMG_BG, dest=[0, 0])
        for square in self.other_squares:
            square.draw()
        rect_fill(
            color=translucented_color(color="black", a=64),
            rect=Rect(0, 0, WX, WY),
        )
        for pq in self.player_squares:
            pq.draw()

    def elapse(self) -> None:
        """時間経過の処理を行います"""
        ...

    def in_progress(self) -> bool:
        return True

    def _player_squares(self) -> list[PlayerSquare]:
        li: list[PlayerSquare] = []
        for square in self.board_view.squares:
            if isinstance(square, PlayerSquare) and square.player !=self.exclude:
                pq = copy(square)
                li.append(pq)
        return li

    def _other_squares(self) -> list[Square]:
        li: list[Square] = []
        for square in self.board_view.squares:
            if not isinstance(square, PlayerSquare):
                li.append(square)
        return li
