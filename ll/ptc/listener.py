from typing import Protocol, runtime_checkable

from model.board import Board
from ptc.view import View
from ptc.notification import Notification

@runtime_checkable
class Listener(Protocol):
    board: Board
    view: View

    def listen(self, nf: Notification) -> None:
        ...