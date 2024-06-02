from typing import Protocol, runtime_checkable

from model.board import Board
from ptc.view import View
from ptc.transition import Transition

@runtime_checkable
class Bridge(Protocol):
    board: Board
    view: View

    def whileloop(self, new_view: Transition) -> None:
        ...