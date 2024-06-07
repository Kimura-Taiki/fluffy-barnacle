from pygame import Surface, transform, Vector2 as V2, mouse, Rect, SRCALPHA
from math import sin, cos, radians

from any.func import ratio_rect, img_zoom, rect_fill, translucented_color, dest_rect_center
from any.mouse_dispatcher import mouse_dispatcher
from any.pictures import IMG_WHITE, IMG_BACK
from any.screen import FRAMES_PER_SECOND
from model.kard import Kard
from model.ui_element import UIElement
from ptc.bridge import Bridge

_RATIO = V2(800, 510)
_SECONDS = 0.1
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.square import Square
class KardSelectSquare():
    def __init__(self, rect: Rect, canvas: Surface) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.img = self._img()
        self.canvas = canvas

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        rect_fill(
            color=translucented_color(color="lightsteelblue"),
            rect=self.rect,
            surface=self.canvas
        )
        self.canvas.blit(
            source=self.img,
            dest=self.rect.topleft
        )

    def _img(self) -> Surface:
        img = Surface(size=_RATIO, flags=SRCALPHA)
        n = 10
        r = 2303
        o_v2 = V2(400, r+240)
        print(f"諸元 : n={n}, r={r}, o_v2={o_v2}")
        for i in range(n):
            deg = -10.0+20.0*i/(n-1)-90.0
            rad = radians(deg)
            i_v2 = o_v2+ie_v2_from_radian(radian=rad)*r
            print(f"座標 : i={i}, deg={deg}, i_v2={i_v2}")
            img_kard = transform.rotozoom(
                surface=IMG_BACK,
                angle=-(deg+90),
                scale=1.0,
            )
            img.blit(
                source=img_kard,
                dest=i_v2-V2(img_kard.get_size())/2
            )
            img.fill(
                color="royalblue",
                rect=Rect(i_v2-V2(16, 16), V2(32, 32))
            )
        return img_zoom(img=img,rect=self.rect, ratio=_RATIO)

def ie_v2_from_radian(radian: float) -> V2:
    return V2(cos(radian), sin(radian))
