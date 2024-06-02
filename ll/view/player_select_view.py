from pygame import Rect
from copy import copy

from any.func import enforce, rect_fill, translucented_color
from any.pictures import IMG_BG
from any.screen import screen, WX, WY, FRAMES_PER_SECOND
from any.timer_functions import frames
from model.player import Player, OBSERVER
from model.ui_element import UIElement
from ptc.bridge import Bridge
from ptc.square import Square
from view.board_view import BoardView
from view.player_square import PlayerSquare

_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class PlayerSelectView:
    def __init__(self, bridge: Bridge, exclude: Player=OBSERVER) -> None:
        self.bridge = bridge
        self.exclude = exclude
        self.board_view = enforce(bridge.view, BoardView)
        self.player_squares = self._player_squares()
        self.other_squares = self._other_squares()
        self.selected_player: Player | None = None
        self.frames = frames()

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
        return bool(not self.selected_player)

    def _player_squares(self) -> list[PlayerSquare]:
        li: list[PlayerSquare] = []
        for square in self.board_view.squares:
            if isinstance(square, PlayerSquare) and square.player != self.exclude:
                li.append(self._player_square(pq=square))
        return li

    def _player_square(self, pq: PlayerSquare) -> PlayerSquare:
        def hover(pq: PlayerSquare) -> None:
            a = int(abs((frames()-self.frames)%(_WAIT*2)-_WAIT)/_WAIT*128)+64
            rect_fill(
                color=translucented_color(color="white", a=a),
                rect=pq.rect
            )
        copy_pq = copy(pq)
        copy_pq.ui_element = UIElement(hover=lambda : hover(pq=copy_pq))
        return copy_pq


    def _other_squares(self) -> list[Square]:
        li: list[Square] = []
        for square in self.board_view.squares:
            if not isinstance(square, PlayerSquare):
                li.append(square)
        return li
