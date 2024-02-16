#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol

from mod.const import pass_func
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat

@runtime_checkable
class OverLayer(Protocol):
    name: str = "------"
    inject_func: Callable[[], None] = pass_func
    delivery: Delivery = duck_delivery

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        ...

    def close(self) -> PopStat:
        ...

    def moderate(self, stat: PopStat) -> None:
        ...
