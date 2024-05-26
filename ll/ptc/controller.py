from typing import runtime_checkable, Protocol, Callable

# from model.board import Board
# from ptc.view import View

@runtime_checkable
class Controller(Protocol):
    # board: Board
    # view: View

    def action(self) -> None:
        ...

    def callback(self) -> None:
        ...