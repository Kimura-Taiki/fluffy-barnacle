from pygame import Rect

from any.screen import screen, WX, WY
from any.pictures import IMG_BG
from model.board import Board
from model.player import Player
from model.ui_element import UIElement
from view.deck_square import DeckSquare
from view.choice_square import ChoiceSquare
from view.player_square import PlayerSquare
from ptc.square import Square
from ptc.bridge import Bridge

_W = WX / 4
_H = WY * 2 / 5
_D = WX * 3 / 16
_C = WX * 6 /16

class BoardView:
    def __init__(self, subject: Player, bridge: Bridge) -> None:
        self.subject = subject
        self.bridge = bridge
        self.deck_square = self._deck_square()
        self.subject_square = self._subject_square()
        self.opponents_squares = self._opponents_squares(opponents=self.board.players)
        self.hand_square = ChoiceSquare(rect=Rect(_D+_W, _H, _C, WY-_H), bridge=self.bridge)
        li = (self.deck_square, self.subject_square, *self.opponents_squares, self.hand_square)
        self.squares: list[Square] = [
            square for square in li
            if square is not None
        ]

    def rearrange(self) -> None:
        """レイアウトの再配置を行います"""
        ...

    def get_hover(self) -> UIElement | None:
        """ホバー中の要素を取得します"""
        for square in self.squares[::-1]:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        """ボードを描画します"""
        screen.blit(source=IMG_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()

    def elapse(self) -> None:
        """時間経過の処理を行います"""
        for square in self.squares:
            square.elapse()

    def _deck_square(self) -> DeckSquare:
        return DeckSquare(deck=self.board.deck, rect=Rect(0, WY - _H, _D, _H))

    def _subject_square(self) -> PlayerSquare | None:
        return PlayerSquare(
            player=self.subject, rect=Rect(_D, WY - _H, _W, _H), bridge=self.bridge,
        ) if self.subject in self.board.players else None

    def _opponents_squares(self, opponents: list[Player]) -> list[PlayerSquare]:
        opponents = [player for player in opponents if player != self.subject]  # 主題を除外
        w = WX / len(opponents)
        return [PlayerSquare(
            player=player,
            rect=Rect(w * i, 0, w, _H),
            bridge=self.bridge,)
            for i, player in enumerate(opponents)
        ]

    @property
    def board(self) -> Board:
        return self.bridge.board
