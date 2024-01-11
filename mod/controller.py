from typing import Callable

# from mod.huda import Huda
from mod.youso import Youso

class Controller():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Youso | None = None
        self.get_hovered: Callable[[], Youso | None] = self._not_implemented_get_hovered
        self.active: Youso | None = None

    @staticmethod
    def _not_implemented_get_hovered() -> None:
        raise NotImplementedError("Controller.get_hoveredが未定義です")

controller = Controller()