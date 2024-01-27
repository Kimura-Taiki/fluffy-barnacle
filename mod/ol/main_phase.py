from typing import Callable, Any

from mod.const import compatible_with, pass_func
from mod.moderator import OverLayer
from mod.youso import Youso

class MainPhase():
    def __init__(self) -> None:
        self.inject_func: Callable[[], None] = pass_func

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        ...

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

compatible_with(MainPhase(), OverLayer)