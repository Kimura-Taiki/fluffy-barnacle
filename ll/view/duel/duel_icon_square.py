from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect, make_progress_funcs
from any.pictures import IMG_DUEL
from any.timer_functions import make_ratio_func
from model.ui_element import UIElement

_RATIO = V2(280, 280)

from ptc.transition import Transition
class DuelIconSquare():
    def __init__(self, rect: Rect, canvas: Surface, seconds: float=0.0) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=seconds) if seconds else lambda: 1.0
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.img_duel = self._img_duel()

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        img_rz = self._img_rz()
        self.canvas.blit(
            source=img_rz,
            dest=V2(self.rect.center)-V2(img_rz.get_size())/2+offset
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def _img_duel(self) -> Surface:
        return transform.rotozoom(surface=IMG_DUEL, angle=0.0, scale=self.rect.w/_RATIO.x)

    def _img_rz(self) -> Surface:
        return transform.rotozoom(
            surface=self.img_duel,
            angle=0.0,
            scale=3.0-self._ratio()*2
        )
