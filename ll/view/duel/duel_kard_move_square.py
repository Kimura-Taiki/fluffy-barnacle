from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect
from any.pictures import IMG_BACK
from any.timer_functions import make_ratio_func
from model.kard import Kard
from model.ui_element import UIElement

_RATIO = V2(340, 475)

from ptc.transition import Transition
class DuelKardMoveSquare():
    def __init__(
            self, rect: Rect, kard: Kard, is_left: bool,
            canvas: Surface, seconds: float=0.0
        ) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self._drawing_in_progress = True
        self.canvas = canvas
        self.img_back = self._img_back()
        self.to_v2 = V2(rect.topleft)
        self.from_v2 = self.to_v2+V2(self.img_back.get_width(), 0)*(-2 if is_left else 2)
        self._ratio = make_ratio_func(seconds=seconds) if seconds else lambda: 1.0

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        self.canvas.blit(
            source=self.img_back,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())+offset
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def in_progress(self) -> bool:
        return self._drawing_in_progress

    def _img_back(self) -> Surface:
        return transform.rotozoom(surface=IMG_BACK, angle=0.0, scale=self.rect.w/_RATIO.x)

    def _complete(self) -> None:
        self._drawing_in_progress = False
