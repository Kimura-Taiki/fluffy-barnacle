from typing import Protocol, runtime_checkable

from model.board import Board
from ptc.view import View

@runtime_checkable
class Bridge(Protocol):
    board: Board
    view: View
