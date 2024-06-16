from pygame import Surface
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class Kard(Protocol):
    def picture(self) -> Surface:
        ...

    def use_func(self, bridge: Any, player: Any) -> None:
        '''
        use_func(Bridge, Player) -> None

        カードを使用した際に起動する命令です。
        第１引数にBridge,第２引数にPlayerを代入してください。
        '''
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def rank(self) -> int:
        ...

    @property
    def view_hash(self) -> tuple[Any, ...]:
        ...

@dataclass
class _EmptyKard():
    def picture(self) -> Surface:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

    def use_func(self, bridge: Any, player: Any) -> None:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

    @property
    def name(self) -> str:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

    @property
    def rank(self) -> int:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

    @property
    def view_hash(self) -> tuple[Any, ...]:
        raise RuntimeError("このクラスは実際の運用を想定していないため、操作ができません。")

EMPTY_KARD = _EmptyKard()
