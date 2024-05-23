from typing import runtime_checkable, Protocol

from ptc.element import Element

@runtime_checkable
class Square(Protocol):
    def get_hover(self) -> Element | None:
        ...

    def draw(self) -> None:
        ...