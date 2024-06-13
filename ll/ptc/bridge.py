from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from model.board import Board
from ptc.view import View, _EmptyView
from ptc.transition import Transition

@runtime_checkable
class Bridge(Protocol):
    board: Board
    view: View

    def whileloop(self, new_view: Transition) -> None:
        ...

@dataclass
class _EmptyBridge():
    board: Board = field(default_factory=Board(players=[]))
    view: View = field(default_factory=_EmptyView())

    raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")
