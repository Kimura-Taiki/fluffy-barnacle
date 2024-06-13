from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from model.board import Board
from ptc.view import View, EMPTY_VIEW
from ptc.transition import Transition

@runtime_checkable
class Bridge(Protocol):
    board: Board
    view: View

    def whileloop(self, new_view: Transition) -> None:
        ...

@dataclass
class _EmptyBridge():
    board: Board = field(default_factory=Board)
    view: View = field(default=EMPTY_VIEW)

    def whileloop(self, new_view: Transition) -> None:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

EMPTY_BRIDGE = _EmptyBridge()
"""Bridge プロトコルの事前定義用のプレースホルダーです。

このインスタンスは、実際の実装が利用可能になる前に Bridge 型の変数を宣言または渡す必要がある場合に便利です。
`whileloop` メソッドが呼び出されると、実際の使用を意図していないことを示す RuntimeError が発生します。
"""