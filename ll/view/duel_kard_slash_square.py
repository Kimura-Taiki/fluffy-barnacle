from pygame import Surface, Vector2 as V2, Rect
from typing import TypeVar

from any.func import ratio_rect, img_zoom, dest_rect_center
from any.screen import FRAMES_PER_SECOND
from any.timer_functions import frames
from model.kard import Kard
from model.ui_element import UIElement

_RATIO = V2(340, 475)

from ptc.transition import Transition
class DuelKardSlashSquare():
    def __init__(
            self, rect: Rect, kard: Kard, canvas: Surface, seconds: float=0.0
        ) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self._drawing_in_progress = True
        self.frames = frames()
        self.canvas = canvas
        self.wait = int(FRAMES_PER_SECOND*seconds)
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

    def in_progress(self) -> bool:
        return self._drawing_in_progress

    def _ratio(self) -> float:
        return 1.0 if self.wait == 0 else (frames()-self.frames)/self.wait

    def _complete(self) -> None:
        self._drawing_in_progress = False
