from typing import Protocol, runtime_checkable

from model.board import Board

@runtime_checkable
class Notification(Protocol):
    code: int
    message: str

    def created_board(self, board: Board) -> Board:
        ...