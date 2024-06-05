from pygame import Surface, Vector2 as V2, Rect

from any.func import ratio_rect, img_zoom, dest_rect_center
from model.kard import Kard
from view.progress_helper import ProgressHelper

_RATIO = V2(340, 475)

from ptc.square import Square
class DuelKardSlashSquare():
    def __init__(
            self, rect: Rect, kard: Kard, canvas: Surface, seconds: float=0.0
        ) -> None:
        self._ratio = ProgressHelper(seconds=seconds).ratio
        self.get_hover = ProgressHelper.empty_get_hover
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
