from pygame import Surface, Vector2 as V2, SRCALPHA, Rect

from any.font import LL_RENDER
from any.func import rect_fill, translucented_color
from any.screen import screen, WX, WY
from view.progress_helper import ProgressHelper

_BAND_H = 24
_FONT = 28
_SECONDS = 1.0
_FI_RATIO = 0.25
_SEE_RATIO = 0.75

from ptc.transition import Transition
class MessageTransition():
    def __init__(
            self, img_mes: Surface | str, canvas: Surface=screen, seconds: float=_SECONDS
    ) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_mes = img_mes if isinstance(img_mes, Surface) else LL_RENDER(img_mes, _FONT, "black")
        self.img_band = self._img_band()
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.canvas.blit(source=self.img_band, dest=(0, WY/2-self.img_band.get_height()/2))
        if self._ratio() < _FI_RATIO:
            from_v2 = self._left_v2
            to_v2 = self._center_v2
            ratio = self._ratio()/_FI_RATIO
        elif self._ratio() < _SEE_RATIO:
            from_v2 = self._center_v2
            to_v2 = from_v2
            ratio = 0.0
        else:
            from_v2 = self._center_v2
            to_v2 = self._right_v2
            ratio = (self._ratio()-_SEE_RATIO)/(1.0-_SEE_RATIO)
        self.canvas.blit(
            source=self.img_mes,
            dest=from_v2.lerp(to_v2, ratio)
        )

    def _img_band(self) -> Surface:
        img = Surface(size=(WX, self.img_mes.get_height()+_BAND_H*2), flags=SRCALPHA)
        rect_fill(color=translucented_color("white"), rect=Rect(0, 0, WX, img.get_height()), surface=img)
        return img

    @property
    def _title_y(self) -> int:
        return int(WY/2-self.img_mes.get_height()/2)

    @property
    def _left_v2(self) -> V2:
        return V2(-self.img_mes.get_width(), self._title_y)

    @property
    def _center_v2(self) -> V2:
        return V2(WX/2-self.img_mes.get_width()/2, self._title_y)

    @property
    def _right_v2(self) -> V2:
        return V2(WX, self._title_y)
