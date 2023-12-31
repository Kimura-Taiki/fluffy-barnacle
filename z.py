from typing import Callable

from mod.huda import Huda

class Mouse():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hovered: Huda | None = None
        self.get_hovered: Callable[[], Huda | None] = self._not_implemented_error

    @staticmethod
    def _not_implemented_error() -> None:
        NotImplementedError("Mouse.get_hoveredが未定義です")
