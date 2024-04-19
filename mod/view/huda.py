from pygame import Surface, Vector2 as V2, transform
from math import sin, cos, radians

from mod.const.screen import screen

class Huda():
    def __init__(self, img: Surface, mid: V2, angle: float, scale: float) -> None:
        hx, hy = V2(img.get_size())/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        self.vertices = [self._rotated_vertices(ov=mid, iv=vec, angle=angle) for vec in li]
        self.img = transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.dest = mid-V2(self.img.get_size())/2

    def is_cursor_on(self) -> bool:
        return False

    def draw(self) -> None:
        screen.blit(source=self.img, dest=self.dest)

    def _rotated_vertices(self, ov: V2, iv: V2, angle: float) -> V2:
        rad = radians(-angle)
        return V2(ov.x+(cos(rad)*iv.x-sin(rad)*iv.y),
                  ov.y+(sin(rad)*iv.x+cos(rad)*iv.y))
