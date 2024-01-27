from typing import Callable, Protocol, Any, runtime_checkable

from mod.const import pass_func

@runtime_checkable
class OverLayer(Protocol):
    inject_func: Callable[[], None]

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        ...

    def close(self) -> int:
        ...

    def moderate(self, stat: int) -> None:
        ...

class Moderator():
    def __init__(self) -> None:
        self.stack: list[OverLayer] = []
        self.inject_funcs: Callable[[], None] = pass_func

    def append(self, over_layer: OverLayer) -> None:
        self.stack.append(over_layer)
        over_layer.open()
        over_layer.inject_func()

    def pop(self) -> None:
        over_layer = self.stack.pop()
        self.stack[-1].inject_func()
        self.stack[-1].moderate(stat=over_layer.close())

moderator = Moderator()