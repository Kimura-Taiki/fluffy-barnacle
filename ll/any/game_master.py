from model.board import Board
from ptc.view import View, EMPTY_VIEW
from ptc.notification import Notification

from ptc.listener import Listener
class GameMaster():
    def __init__(self, board: Board, view: View=EMPTY_VIEW) -> None:
        self.board = board
        self.view = view

    def listen(self, nf: Notification) -> None:
        self.board = nf.created_board(board=self.board)
