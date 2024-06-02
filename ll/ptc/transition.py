from typing import Protocol, runtime_checkable

from model.ui_element import UIElement

@runtime_checkable
class Transition(Protocol):
    def get_hover(self) -> UIElement | None:
        ...

    def draw(self) -> None:
        ...

    def elapse(self) -> None:
        ...

    def in_progress(self) -> bool:
        ...