from typing import Protocol, runtime_checkable

from model.player import Player
from model.ui_element import UIElement

@runtime_checkable
class MainView(Protocol):
    subject: Player

    def get_hover(self) -> UIElement | None:
        ...

    def draw(self) -> None:
        ...

    def elapse(self) -> None:
        ...

