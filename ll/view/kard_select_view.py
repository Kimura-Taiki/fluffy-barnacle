from pygame import Surface, Vector2 as V2, Rect, SRCALPHA
from math import sin, cos, radians

from any.func import ratio_rect, img_zoom, rect_fill, translucented_color
from any.screen import screen, WV2
from model.deck import _kards
from model.ui_element import UIElement
from ptc.bridge import Bridge
from view.kard_square import KardSquare

_RATIO = V2(1280, 640)

from ptc.transition import Transition
class KardSelectView():
    def __init__(
            self, bridge: Bridge, rect: Rect=Rect((0, 0), WV2),
            canvas: Surface=screen
        ) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.view = bridge.view
        self.img = self._img()
        self.squares = self._squares()

    def get_hover(self) -> UIElement | None:
        for square in self.squares[::-1]:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        self.view.draw()
        rect_fill(
            color=translucented_color(color="black", a=64),
            rect=Rect((0, 0), WV2),
            surface=self.canvas
        )
        # rect_fill(
        #     color=translucented_color(color="lightsteelblue"),
        #     rect=self.rect,
        #     surface=self.canvas
        # )
        self.canvas.blit(
            source=self.img,
            dest=self.rect.topleft
        )
        for square in self.squares:
            square.draw()

    def elapse(self) -> None:
        for square in self.squares:
            square.elapse()

    def in_progress(self) -> bool:
        return True

    def _img(self) -> Surface:
        img = Surface(size=_RATIO, flags=SRCALPHA)
        return img_zoom(img=img,rect=self.rect, ratio=_RATIO)

    def _squares(self) -> list[KardSquare]:
        li: list[KardSquare] = []
        n = 7
        r = 2303
        o_v2 = V2(640, r+375)
        for i in range(n):
            deg = -10.0+20.0*i/(n-1)-90.0
            rad = radians(deg)
            i_v2 = o_v2+ie_v2_from_radian(radian=rad)*r
            li.append(KardSquare(
                kard=_kards[i+2],
                angle=-(deg+90),
                scale=self.rect.w/_RATIO.x,
                center=i_v2,
                canvas=self.canvas,
                mousedown=lambda : None
            ))
        return li


def ie_v2_from_radian(radian: float) -> V2:
    return V2(cos(radian), sin(radian))
