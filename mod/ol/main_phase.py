from typing import Callable, Any

from mod.const import compatible_with, pass_func
from mod.moderator import OverLayer
from mod.youso import Youso
from mod.popup_message import popup_message

class MainPhase():
    def __init__(self) -> None:
        self.inject_func: Callable[[], None] = pass_func

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