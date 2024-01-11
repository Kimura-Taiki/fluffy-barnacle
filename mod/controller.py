from typing import Callable

from mod.huda import Huda

class Controller():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Huda | None = None
        self.get_hovered: Callable[[], Huda | None] = self._not_implemented_get_hovered
        self.active: Huda | None = None

    @staticmethod
    def _not_implemented_get_hovered() -> None:
        raise NotImplementedError("Controller.get_hoveredが未定義です")

controller = Controller()