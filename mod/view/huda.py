from pygame import Surface, Vector2 as V2, transform, mouse
from math import sin, cos, radians
from typing import Callable, Any
from functools import partial

def _hoge(any: Any) -> None:
    ...

class Huda():
    def __init__(self, img: Surface, mid: V2, angle: float, scale: float,
    draw: Callable[['Huda'], None]=_hoge, hover: Callable[['Huda'], None]=_hoge,
    mousedown: Callable[['Huda'], None]=_hoge, active: Callable[['Huda'], None]=_hoge,
    mouseup: Callable[['Huda'], None]=_hoge, drag: Callable[['Huda'], None]=_hoge,
    dragend: Callable[['Huda'], None]=_hoge) -> None:
        hx, hy = V2(img.get_size())*scale/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        self.vertices = [self._rotated_vertices(ov=mid, iv=vec, angle=angle) for vec in li]
        self.img = transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.img_hover = img
        self.dest = mid-V2(self.img.get_size())/2
        self.angle = angle
        self.draw: Callable[[], None] = partial(draw, self)
        self.hover: Callable[[], None] = partial(hover, self)
        self.mousedown: Callable[[], None] = partial(mousedown, self)
        self.active: Callable[[], None] = partial(active, self)
        self.mouseup: Callable[[], None] = partial(mouseup, self)
        self.drag: Callable[[], None] = partial(drag, self)
        self.dragend: Callable[[], None] = partial(dragend, self)

    def is_cursor_on(self) -> bool:
        inside = False
        mx, my = mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return inside

    def _rotated_vertices(self, ov: V2, iv: V2, angle: float) -> V2:
        rad = radians(-angle)
        return V2(ov.x+(cos(rad)*iv.x-sin(rad)*iv.y),
                  ov.y+(sin(rad)*iv.x+cos(rad)*iv.y))
