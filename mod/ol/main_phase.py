from typing import Callable, Any

from mod.const import compatible_with, pass_func
from mod.over_layer import OverLayer
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.delivery import Delivery, duck_delivery

class MainPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "メインフェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        popup_message.add(text="MainPhase.openで開いたよ")

    def close(self) -> int:
        popup_message.add(text="MainPhase.closeで閉じたよ")
        return 0

    def moderate(self, stat: int) -> None:
        ...

compatible_with(MainPhase(), OverLayer)