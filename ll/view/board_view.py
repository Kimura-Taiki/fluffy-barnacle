from pygame import Rect

from mod.screen import screen, IMG_BG, WX, WY
from model.board import Board
from view.player_square import PlayerSquare
from view.deck_square import DeckSquare
from mod.router import router
from ptc.player import Player
from ptc.element import Element
from ptc.square import Square
from ptc.listener import Listener

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
        router.mouse_over()
        # if hover := self.get_hover():
        #     screen.fill(color=(255, 0, 0), rect=((hover.dest)-(10, 10), (20, 20)))

    def _squares(self) -> list[Square]:
        opponents = [player for player in self.board.players if player != self.subject]
        w = WX/len(opponents)
        h = WY*2/5
        d = WX*3/16
        opponents_squares: list[Square] = [
            PlayerSquare(player=player, rect=Rect(w*i, 0, w, h), listener=self.listener)
            for i, player in enumerate(opponents)]
        subject_square: list[Square] = [
            PlayerSquare(player=self.subject, rect=Rect(w/2, WY-h, w, h), listener=self.listener)
            ] if self.subject in self.board.players else []
        deck_square: list[Square] = [DeckSquare(deck=self.board.deck, rect=Rect(0, WY-h, d, h))]
        return opponents_squares+subject_square+deck_square
