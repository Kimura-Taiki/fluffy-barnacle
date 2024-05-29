from typing import Callable
from dataclasses import dataclass

@dataclass
class UIElement():
    hover: Callable[[], None] = lambda : None
    mousedown: Callable[[], None] = lambda : None
    active: Callable[[], None] = lambda : None
    mouseup: Callable[[], None] = lambda : None
    drag: Callable[[], None] = lambda : None
    dragend: Callable[[], None] = lambda : None
