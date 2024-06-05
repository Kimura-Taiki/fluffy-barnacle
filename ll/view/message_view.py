from pygame import Surface, Vector2 as V2, SRCALPHA, Rect

from any.func import rect_fill, translucented_color
from any.screen import screen, WX, WY
from view.board_view import BoardView
from view.progress_helper import ProgressHelper

_FADE_IN_SECONDS = 0.25
_SEEING_SECONDS = 0.5
_FADE_OUT_SECONDS = 0.25
_TOTAL_SECONDS = _FADE_IN_SECONDS+_SEEING_SECONDS+_FADE_OUT_SECONDS
_FI_RATIO = _FADE_IN_SECONDS/_TOTAL_SECONDS
_SEE_RATIO = (_FADE_IN_SECONDS+_SEEING_SECONDS)/_TOTAL_SECONDS
_BAND_H = 24

from ptc.view import View
class MessageView():
    def __init__(self, board_view: BoardView, img_mes: Surface) -> None:
        self._ratio, self.in_progress, _, _, self.get_hover, self.elapse\
            = ProgressHelper(seconds=_TOTAL_SECONDS).provide_progress_funcs()
        self.board_view = board_view
        self.img_mes = img_mes
        self.img_band = self._img_band()

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(source=self.img_band, dest=(0, WY/2-self.img_band.get_height()/2))
        if self._ratio() < _FI_RATIO:
            from_v2 = self._left_v2()
            to_v2 = self._center_v2()
            ratio = self._ratio()/_FI_RATIO
        elif self._ratio() < _SEE_RATIO:
            from_v2 = self._center_v2()
            to_v2 = from_v2
            ratio = 0.0
        else:
            from_v2 = self._center_v2()
            to_v2 = self._right_v2()
            ratio = (self._ratio()-_SEE_RATIO)/(1.0-_SEE_RATIO)
        screen.blit(
            source=self.img_mes,
            dest=from_v2.lerp(to_v2, ratio)
        )

    def _img_band(self) -> Surface:
        img = Surface(size=(WX, self.img_mes.get_height()+_BAND_H*2), flags=SRCALPHA)
        rect_fill(color=translucented_color("white"), rect=Rect(0, 0, WX, img.get_height()), surface=img)
        return img

    def _title_y(self) -> int:
        return int(WY/2-self.img_mes.get_height()/2)

    def _left_v2(self) -> V2:
        return V2(-self.img_mes.get_width(), self._title_y())

    def _center_v2(self) -> V2:
        return V2(WX/2-self.img_mes.get_width()/2, self._title_y())

    def _right_v2(self) -> V2:
        return V2(WX, self._title_y())
