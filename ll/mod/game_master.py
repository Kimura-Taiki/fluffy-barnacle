from mod.board import Board
from ptc.view import View, EMPTY_VIEW

class GameMaster():
    def __init__(self, board: Board, view: View=EMPTY_VIEW) -> None:
        self.board = board
        self.view = view