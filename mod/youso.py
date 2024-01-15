from typing import Callable
from functools import partial

from mod.const import pass_func

class Youso():
    def __init__(self, **kwargs) -> None:
        self.draw: Callable[..., None] = partial(kwargs.get('draw', pass_func), self)
        self.hover: Callable[..., None] = partial(kwargs.get('hover', pass_func), self)
        self.mousedown: Callable[..., None] = partial(kwargs.get('mousedown', pass_func), self)
        self.active: Callable[..., None] = partial(kwargs.get('active', pass_func), self)
        self.mouseup: Callable[..., None] = partial(kwargs.get('mouseup', pass_func), self)
        self.dragstart: Callable[..., None] = partial(kwargs.get('dragstart', pass_func), self)
        self.drag: Callable[..., None] = partial(kwargs.get('drag', pass_func), self)
        self.dragend: Callable[..., None] = partial(kwargs.get('dragend', pass_func), self)
