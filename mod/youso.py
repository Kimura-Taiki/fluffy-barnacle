from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any
from functools import partial
from typing import Any

from mod.const import pass_func, compatible_with
from mod.delivery import Delivery, Listener, duck_delivery

class Youso():
    def __init__(self, x: int|float=0, y: int|float=0, **kwargs: Callable[..., None]) -> None:
        self.x = x
        self.y = y
        self.delivery: Delivery = duck_delivery
        self.draw: Callable[..., None]
        self.hover: Callable[..., None]
        self.mousedown: Callable[..., None]
        self.active: Callable[..., None]
        self.mouseup: Callable[..., None]
        self.dragstart: Callable[..., None]
        self.drag: Callable[..., None]
        self.dragend: Callable[..., None]
        self.inject_funcs(**kwargs)

    def inject_funcs(self, **kwargs: Callable[..., None]) -> None:
        self.draw = partial(kwargs.get('draw', pass_func), self)
        self.hover = partial(kwargs.get('hover', pass_func), self)
        self.mousedown = partial(kwargs.get('mousedown', pass_func), self)
        self.active = partial(kwargs.get('active', pass_func), self)
        self.mouseup = partial(kwargs.get('mouseup', pass_func), self)
        self.dragstart = partial(kwargs.get('dragstart', pass_func), self)
        self.drag = partial(kwargs.get('drag', pass_func), self)
        self.dragend = partial(kwargs.get('dragend', pass_func), self)

    def set_partial_attr(self, attr: str, func: Callable[[Any], None]) -> bool | None:
        setattr(self, attr, partial(func, self))
        return None

    def topleft(self, source: Surface) -> Vector2:
        return self.dest-Vector2(source.get_size())/2
    
    def tenko(self) -> list[Listener]:
        return [self]

    @property
    def dest(self) -> Vector2:
        return Vector2(self.x, self.y)
    
    @dest.setter
    def dest(self, x:int | float, y:int | float) -> None:
        self.x, self.y = int(x), int(y)

compatible_with(obj=Youso(), protocol=Listener)
