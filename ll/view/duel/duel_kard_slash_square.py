from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect, img_zoom, dest_rect_center, make_progress_funcs
from any.timer_functions import make_ratio_func
from model.kard import Kard
from model.ui_element import UIElement

_RATIO = V2(340, 475)

from ptc.transition import Transition
class DuelKardSlashSquare():
    def __init__(
            self, rect: Rect, kard: Kard, canvas: Surface, seconds: float=0.0
        ) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=seconds)
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self.canvas = canvas
        self.img_front = img_zoom(
            img=kard.picture(),
            rect=self.rect,
            ratio=_RATIO
        )

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        img = self.img_front
        w, h = int(img.get_width()/2), img.get_height()
        dv = V2(0, h*self._ratio())
        img.set_alpha(int(255-255*self._ratio()))
        self.canvas.blit(
            source=img,
            dest=dest_rect_center(rect=self.rect, img=img)-dv+offset,
            area=Rect(0, 0, w, h)
        )
        self.canvas.blit(
            source=img,
            dest=dest_rect_center(rect=self.rect, img=img)+V2(w,0)+dv+offset,
            area=Rect(w, 0, w, h)
        )
        img.set_alpha(255)

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()
