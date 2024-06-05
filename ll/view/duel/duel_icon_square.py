from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect
from any.pictures import IMG_DUEL
from view.progress_helper import ProgressHelper

_RATIO = V2(280, 280)

from ptc.transition import Transition
class DuelIconSquare():
    def __init__(self, rect: Rect, canvas: Surface, seconds: float=0.0) -> None:
        self._ratio = ProgressHelper(seconds=seconds).ratio
        self._ratio = self._ratio if seconds else lambda : 1.0
        self.get_hover = ProgressHelper.empty_get_hover
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.img_duel = self._img_duel()

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        img_rz = self._img_rz()
        self.canvas.blit(
            source=img_rz,
            dest=V2(self.rect.center)-V2(img_rz.get_size())/2+offset
        )

    def _img_duel(self) -> Surface:
        return transform.rotozoom(surface=IMG_DUEL, angle=0.0, scale=self.rect.w/_RATIO.x)

    def _img_rz(self) -> Surface:
        return transform.rotozoom(
            surface=self.img_duel,
            angle=0.0,
            scale=3.0-self._ratio()*2
        )
