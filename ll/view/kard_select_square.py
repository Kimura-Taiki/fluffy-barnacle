from pygame import Surface, transform, Vector2 as V2, mouse, Rect, SRCALPHA
from math import sin, cos, radians

from any.func import ratio_rect, img_zoom, rect_fill, translucented_color
from any.mouse_dispatcher import mouse_dispatcher
from any.pictures import IMG_WHITE
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
        return img_zoom(img=img,rect=self.rect, ratio=_RATIO)
