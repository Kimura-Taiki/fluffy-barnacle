from typing import Protocol, runtime_checkable

from model.ui_element import UIElement

@runtime_checkable
class View(Protocol):
    def get_hover(self) -> UIElement | None:
        ...

    def draw(self) -> None:
        ...

    def elapse(self) -> None:
        ...

class _EmptyView():
    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        pass

    def elapse(self) -> None:
        pass

EMPTY_VIEW = _EmptyView()
