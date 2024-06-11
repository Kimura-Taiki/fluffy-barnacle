from pygame import Surface
from typing import Protocol, runtime_checkable, Callable, Any

@runtime_checkable
class Kard(Protocol):
    png_file: str
    picture: Callable[[], Surface]
    name: str
    rank: int
    board_func: Callable[[Any], None]