from typing import Callable
from functools import partial

from mod.const import pass_func

class Youso():
    def __init__(self, hover: Callable[..., None]=pass_func) -> None:
        self.hover: Callable[..., None] = partial(hover, self)
