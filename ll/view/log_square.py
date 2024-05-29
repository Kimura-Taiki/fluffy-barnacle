from pygame import Rect, Surface, SRCALPHA, transform

from any.func import ratio_rect
from model.kard import Kard
from model.ui_element import UIElement

from ptc.square import Square
class LogSquare():
    _RATIO = (136, 190)

    def __init__(self, kard: Kard, rect: Rect, canvas: Surface) -> None:
        self.kard = kard
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.img = self._img()
        self.canvas = canvas

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        self.canvas.blit(source=self.img, dest=self.rect)

    def elapse(self) -> None:
        ...

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        img.blit(
            source=transform.rotozoom(
                surface=self.kard.picture(),
                angle=0.0, scale=0.4),
            dest=(0, 0))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
