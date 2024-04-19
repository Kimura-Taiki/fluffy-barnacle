from typing import runtime_checkable, Protocol

@runtime_checkable
class Element(Protocol):
    def is_cursor_on(self) -> bool:
        ...

    def draw(self) -> None:
        ...
