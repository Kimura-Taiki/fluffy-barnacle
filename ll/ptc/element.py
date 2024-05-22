from typing import runtime_checkable, Protocol, Callable

@runtime_checkable
class Element(Protocol):
    # draw: Callable[[], None]
    hover: Callable[[], None]
    mousedown: Callable[[], None]
    active: Callable[[], None]
    mouseup: Callable[[], None]
    drag: Callable[[], None]
    dragend: Callable[[], None]

    # def is_cursor_on(self) -> bool:
    #     ...
