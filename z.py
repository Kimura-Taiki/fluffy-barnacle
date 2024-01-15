from pygame.math import Vector2 as v2

v = v2(3, 4)
w = v2(12, 5)
print(v.magnitude())
print(v2((12, 5)).magnitude())
print(v2(16,9)/2)

class Youso():
    def __init__(self, draw: Callable[..., None], hover: Callable[..., None]=pass_func,
                 dragstart: Callable[..., None]=pass_func, drag: Callable[..., None]=pass_func,
                 dragend: Callable[..., None]=pass_func)  -> None:
        self.draw: Callable[..., None] = partial(draw, self)
        self.hover: Callable[..., None] = partial(hover, self)
        self.active: Callable[..., None] = partial(active, self)
        self.dragstatrt: Callable[..., None] = partial(dragstart, self)
        self.drag: Callable[..., None] = partial(drag, self)
        self.dragend: Callable[..., None] = partial(dragend, self)


class Huda(Youso):
    def __init__(self, img: Surface, angle: float=0.0, scale: float=0.4, x:int | float=0, y:int | float=0,
                 draw: Callable[..., None]=default_draw, hover: Callable[..., None]=pass_func,
                 dragstart: Callable[..., None]=pass_func, drag: Callable[..., None]=pass_func,
                 dragend: Callable[..., None]=pass_func) -> None:
        super().__init__(draw=draw, hover=hover, dragstart=dragstart, drag=drag, dragend=dragend)
