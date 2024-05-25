from pygame import Rect

from any.screen import screen, IMG_BG, WX, WY
from any.propagation import propagation
from any.font import MS_MINCHO_COL
from model.board import Board
from model.player import Player
from view.player_square import PlayerSquare
from view.deck_square import DeckSquare
from view.board_view import BoardView
from ptc.element import Element
from ptc.square import Square
from ptc.listener import Listener

from ptc.view import View
class DrawView():
    def __init__(self, board: Board, subject: Player, listener: Listener) -> None:
        self.board_view = BoardView(board=board, subject=subject, listener=listener)
        self.listener = listener

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(
            source=MS_MINCHO_COL("in drawing...", 64, "black"),
            dest=(WX/2-112, WY/2-32)
        )
        propagation.mouse_over()
