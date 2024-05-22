from mod.board import Board
from ptc.view import View, EMPTY_VIEW
from ptc.notification import Notification
from ptc.listener import Listener

class GameMaster():
    def __init__(self, board: Board, view: View=EMPTY_VIEW) -> None:
        self.board = board
        self.view = view

    def listen(self, nf: Notification) -> None:
        raise NotImplementedError(f"まだlistenできないよ！ Code:{nf.code}, Message:{nf.message}")