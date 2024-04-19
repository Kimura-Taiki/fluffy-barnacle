from typing import runtime_checkable, Protocol, Callable

@runtime_checkable
class Element(Protocol):
    draw: Callable[[], None]

    def is_cursor_on(self) -> bool:
        ...

    # def draw(self) -> None:
    #     ...
