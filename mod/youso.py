from typing import Callable
from functools import partial

from mod.const import pass_func

class Youso():
    def __init__(self, hovered: Callable[..., None]=pass_func) -> None:
        self.hovered: Callable[..., None] = partial(hovered, self)
