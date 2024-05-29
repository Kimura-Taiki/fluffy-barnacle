from typing import runtime_checkable, Protocol

from model.ui_element import UIElement

@runtime_checkable
class Square(Protocol):
    def get_hover(self) -> UIElement | None:
        ...

    def draw(self) -> None:
        ...