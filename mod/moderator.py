from typing import Callable, Protocol, Any

from mod.const import pass_func, MC_BEGINNING

class OverLayer(Protocol):
    inject_kwargs: dict[str, Callable[[Any], None]]

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
        self.inject_funcs: Callable[[dict[str, Callable[[Any], None]]], None] = pass_func

    def append(self, over_layer: OverLayer) -> None:
        self.stack.append(over_layer)
        over_layer.open()
        self.inject_funcs(over_layer.inject_kwargs)

    def pop(self) -> None:
        over_layer = self.stack.pop()
        self.inject_funcs(self.stack[-1].inject_kwargs)
        self.stack[-1].moderate(stat=over_layer.close())

moderator = Moderator()