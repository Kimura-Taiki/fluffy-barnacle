from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect
from any.pictures import IMG_BACK
from model.kard import Kard
from view.progress_helper import ProgressHelper

_RATIO = V2(340, 475)

from ptc.square import Square
class DuelKardMoveSquare():
    def __init__(
            self, rect: Rect, kard: Kard, is_left: bool,
            canvas: Surface, seconds: float=0.0
        ) -> None:
        self._ratio = ProgressHelper(seconds=seconds).ratio
        self._ratio = self._ratio if seconds else lambda: 1.0
        self.get_hover = ProgressHelper.empty_get_hover
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self.canvas = canvas
        self.img_back = self._img_back()
        self.to_v2 = V2(rect.topleft)
        self.from_v2 = self.to_v2+V2(self.img_back.get_width(), 0)*(-2 if is_left else 2)

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        self.canvas.blit(
            source=self.img_back,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())+offset
        )

    def _img_back(self) -> Surface:
        return transform.rotozoom(surface=IMG_BACK, angle=0.0, scale=self.rect.w/_RATIO.x)
