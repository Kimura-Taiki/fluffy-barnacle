from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any
from functools import partial

from mod.const import pass_func

class Youso():
    def __init__(self, x: int|float=0, y: int|float=0, **kwargs) -> None:
        self.x = x
        self.y = y
    # def __init__(self, **kwargs) -> None:
    #     self.x: int | float = kwargs.get('x')
    #     self.y: int | float = kwargs.get('y')
        self.draw: Callable[..., None] = partial(kwargs.get('draw', pass_func), self)
        self.hover: Callable[..., None] = partial(kwargs.get('hover', pass_func), self)
        self.mousedown: Callable[..., None] = partial(kwargs.get('mousedown', pass_func), self)
        self.active: Callable[..., None] = partial(kwargs.get('active', pass_func), self)
        self.mouseup: Callable[..., None] = partial(kwargs.get('mouseup', pass_func), self)
        self.dragstart: Callable[..., None] = partial(kwargs.get('dragstart', pass_func), self)
        self.drag: Callable[..., None] = partial(kwargs.get('drag', pass_func), self)
        self.dragend: Callable[..., None] = partial(kwargs.get('dragend', pass_func), self)

    def set_partial_attr(self, attr: str, func: Callable[[Any], None]) -> None:
        setattr(self, attr, partial(func, self))

    def topleft(self, source: Surface) -> Vector2:
        return self.dest-Vector2(source.get_size())/2

    @property
    def dest(self) -> Vector2:
        return Vector2(self.x, self.y)
    
    @dest.setter
    def dest(self, x:int | float, y:int | float) -> None:
        self.x, self.y = int(x), int(y)
