from pygame import Rect, Color, Surface, SRCALPHA, transform, image
from copy import deepcopy

from mod.func import ratio_rect
from mod.kard import Kard
from ptc.square import Square
from ptc.player import Player
from ptc.element import Element

class LogSquare():
    _RATIO = (136, 190)

    def __init__(self, kard: Kard, rect: Rect, canvas: Surface) -> None:
        self.kard = kard
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.img = self._img()
        self.canvas = canvas

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        self.canvas.blit(source=self.img, dest=self.rect)

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        img.blit(
            source=transform.rotozoom(
                surface=image.load(f"ll/pic/{self.kard.png_file}").convert_alpha(),
                angle=0.0, scale=0.4),
            dest=(0, 0))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
