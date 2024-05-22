from pygame import Rect

from mod.screen import screen, IMG_BG, WX, WY
from mod.board import Board
# from mod.view.tehuda_square import TehudaSquare
# from mod.view.crb_square import CrbSquare
from ptc.player import Player
from ptc.element import Element
from ptc.square import Square
from mod.player_square import PlayerSquare

# from pygame import Rect
# from mod.card import Card
from mod.router import router

class BoardView():
    def __init__(self, board: Board, subject: Player) -> None:
        self.board = board
        self.subject = subject
        self.squares = self._squares()
        # self.squares: list[Square] = [
        #     TehudaSquare(bmn.taba(hs=1, cr=CR_TEHUDA), Rect(340, 480, 600, 240)),
        #     TehudaSquare(bmn.taba(hs=2, cr=CR_TEHUDA), Rect(340, 0, 600, 240), True),
        #     CrbSquare(Rect(0, 480, 280, 240)),
        #     CrbSquare(Rect(1000, 0, 280, 240), True)]

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
        # d = WX/
        opponents_squares: list[Square] = [PlayerSquare(player=player, rect=Rect(w*i, 0, w, h)) for i, player in enumerate(opponents)]
        subject_square: list[Square] = [PlayerSquare(player=self.subject, rect=Rect(w/2, WY-h, w, h))] if self.subject in self.board.players else []

        return opponents_squares+subject_square
