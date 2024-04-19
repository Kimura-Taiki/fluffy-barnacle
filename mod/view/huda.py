from pygame import Surface, Vector2 as V2, transform, mouse
from math import sin, cos, radians

from mod.const.screen import screen

class Huda():
    def __init__(self, img: Surface, mid: V2, angle: float, scale: float) -> None:
        hx, hy = V2(img.get_size())*scale/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        self.vertices = [self._rotated_vertices(ov=mid, iv=vec, angle=angle) for vec in li]
        self.img = transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.dest = mid-V2(self.img.get_size())/2
        self.angle = angle

    def is_cursor_on(self) -> bool:
        inside = False
        mx, my = mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return inside

    def draw(self) -> None:
        rad = radians(-self.angle-90.0)
        dest = self.dest+V2(cos(rad), sin(rad))*(40.0 if self.is_cursor_on() else 0.0)
        screen.blit(source=self.img, dest=dest)

    def _rotated_vertices(self, ov: V2, iv: V2, angle: float) -> V2:
        rad = radians(-angle)
        return V2(ov.x+(cos(rad)*iv.x-sin(rad)*iv.y),
                  ov.y+(sin(rad)*iv.x+cos(rad)*iv.y))
