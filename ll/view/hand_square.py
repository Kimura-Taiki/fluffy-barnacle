from pygame import Surface, transform, Vector2 as V2, mouse
from math import sin, cos, radians

from model.kard import Kard
from ptc.bridge import Bridge

from ptc.square import Square
from ptc.element import Element
class HandSquare():
    def __init__(self, kard: Kard, angle: float, scale: float, center: V2, bridge: Bridge, canvas: Surface) -> None:
        self.kard = kard
        self.angle = angle
        self.scale = scale
        self.center = center
        self.bridge = bridge
        self.canvas = canvas
        self.img = self._img()
        self.vertices = self._vertices()
        self.draw = self._draw
        self.hover = lambda: None
        self.mousedown = self._mousedown
        # self.mousedown = lambda: None
        self.active = lambda: None
        self.mouseup = lambda: None
        self.drag = lambda: None
        self.dragend = lambda: None

    def get_hover(self) -> Element | None:
        inside = False
        mx, my = mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return self if inside else None

    def _draw(self) -> None:
        self.canvas.blit(
            source=self.img,
            dest=self.center-V2(self.img.get_size())/2
        )
        for v2 in self.vertices:
            self.canvas.fill(
                color="red",
                rect=((v2-V2(10, 10)), (20, 20))
            )

    def _img(self) -> Surface:
        return transform.rotozoom(
            surface=self.kard.picture(),
            angle=self.angle,
            scale=self.scale
        )

    def _vertices(self) -> list[V2]:
        hx, hy = V2(self.kard.picture().get_size())/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        return [self._rotated_vertices(v2*self.scale) for v2 in li]
    
    def _rotated_vertices(self, from_v2: V2) -> V2:
        rad = radians(-self.angle)
        return V2(
            self.center.x+(cos(rad)*from_v2.x-sin(rad)*from_v2.y),
            self.center.y+(sin(rad)*from_v2.x+cos(rad)*from_v2.y),
        )
    
    def _mousedown(self) -> None:
        raise EOFError(self.kard)
