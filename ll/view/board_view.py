from pygame import Rect, Vector2 as V2

from any.screen import screen, WX, WY
from any.pictures import IMG_BG
from any.propagation import propagation
from model.board import Board
from model.player import Player
from view.player_square import PlayerSquare
from view.deck_square import DeckSquare
from ptc.element import Element
from ptc.square import Square
from ptc.listener import Listener

_H = WY*2/5
_D = WX*3/16

from ptc.view import View
class BoardView():
    def __init__(self, board: Board, subject: Player, listener: Listener) -> None:
        self.board = board
        self.subject = subject
        self.listener = listener
        self.squares = self._squares()

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        for square in self.squares:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        screen.blit(source=IMG_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()
        propagation.mouse_over()
        # if hover := self.get_hover():
        #     screen.fill(color=(255, 0, 0), rect=((hover.dest)-(10, 10), (20, 20)))

    def _squares(self) -> list[Square]:
        opponents = [player for player in self.board.players if player != self.subject]
        # w = WX/len(opponents)
        # h = WY*2/5
        # d = WX*3/16
        ds = DeckSquare(deck=self.board.deck, rect=Rect(0, WY-_H, _D, _H))
        deck_square: list[Square] = [ds]
        opponents_squares = self._opponents_squares(opponents=opponents)
        # opponents_squares: list[Square] = [
        #     PlayerSquare(player=player, rect=Rect(w*i, 0, w, h), listener=self.listener,)
        #     for i, player in enumerate(opponents)]
        subject_square: list[Square] = [
            PlayerSquare(player=self.subject, rect=Rect(_D, WY-_H, WX/4, _H), listener=self.listener,)
            ] if self.subject in self.board.players else []
        return opponents_squares+subject_square+deck_square

    def _opponents_squares(self, opponents: list[Player]) -> list[Square]:
        w = WX/len(opponents)
        li: list[Square] = [PlayerSquare(
            player=player,
            rect=Rect(w*i, 0, w, _H),
            listener=self.listener,)
            for i, player in enumerate(opponents)]
        return li
