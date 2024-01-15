from typing import Callable
from functools import partial

from mod.const import pass_func

# class Youso():
    # def __init__(self, draw: Callable[..., None], hover: Callable[..., None]=pass_func, active: Callable[..., None]=pass_func,
    #              dragstart: Callable[..., None]=pass_func, drag: Callable[..., None]=pass_func,
    #              dragend: Callable[..., None]=pass_func)  -> None:
    #     self.draw: Callable[..., None] = partial(draw, self)
    #     self.hover: Callable[..., None] = partial(hover, self)
    #     self.active: Callable[..., None] = partial(active, self)
    #     self.dragstatrt: Callable[..., None] = partial(dragstart, self)
    #     self.drag: Callable[..., None] = partial(drag, self)
    #     self.dragend: Callable[..., None] = partial(dragend, self)

# class Youso():
#     def __init__(self, draw: Callable[..., None], **kwargs) -> None:
class Youso():
    def __init__(self, **kwargs) -> None:
        self.draw: Callable[..., None] = partial(kwargs.get('draw', pass_func), self)
        self.hover: Callable[..., None] = partial(kwargs.get('hover', pass_func), self)
        self.dragstart: Callable[..., None] = partial(kwargs.get('dragstart', pass_func), self)
        self.drag: Callable[..., None] = partial(kwargs.get('drag', pass_func), self)
        self.dragend: Callable[..., None] = partial(kwargs.get('dragend', pass_func), self)
