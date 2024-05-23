from model.board import Board
from nf.nf_code import NFC_EXIT

from ptc.notification import Notification
class NfExit():
    code: int = NFC_EXIT

    def __init__(self, mes: str="終了コードです") -> None:
        self.message = mes

    def created_board(self, board: Board) -> Board:
        raise NotImplementedError(f"まだlistenできないよ！ Code:{self.code}, Message:{self.message}")
        return board