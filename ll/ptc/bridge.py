from typing import Protocol, runtime_checkable, Callable

from model.board import Board
from ptc.view import View

@runtime_checkable
class Bridge(Protocol):
    board: Board
    view: View

    def whileloop(self, cond: Callable[[], bool]) -> None:
        ...