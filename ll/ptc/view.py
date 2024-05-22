from typing import Protocol, runtime_checkable

from ptc.element import Element

@runtime_checkable
class View(Protocol):
    def get_hover(self) -> Element | None:
        ...

    def draw(self) -> None:
        ...
