from pygame import Surface, Vector2 as V2, SRCALPHA, Rect
from typing import Callable

from any.font import MS_MINCHO_COL
from any.func import rect_fill
from any.screen import screen, WX, WY, FRAMES_PER_SECOND
from any.timer_functions import frames
from ptc.element import Element
from view.board_view import BoardView

_FADE_IN_SECONDS = 0.1
_SEEING_SECONDS = 0.3
_FADE_OUT_SECONDS = 0.1
_WAIT = int(
    FRAMES_PER_SECOND*(
        _FADE_IN_SECONDS+_SEEING_SECONDS+_FADE_OUT_SECONDS
    )
)
_FI_RATIO = (FRAMES_PER_SECOND*_FADE_IN_SECONDS)/_WAIT
_SEE_RATIO = (FRAMES_PER_SECOND*(_FADE_IN_SECONDS+_SEEING_SECONDS))/_WAIT
_FONT_H = 96
_BAND_H = int(_FONT_H*1.5)

from ptc.view import View
class TurnStartView():
    def __init__(self, board_view: BoardView, callback: Callable[[], None]) -> None:
        self.board_view = board_view
        self.callback = callback
        self.img_band = self._img_band()
        self.img_title = self._img_title()
        self.frames = frames()

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(source=self.img_band, dest=(0, WY/2-_BAND_H/2))
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
            to_v2 = self._left_v2()
            ratio = (self._ratio()-_SEE_RATIO)/(_WAIT-_SEE_RATIO)
        screen.blit(
            source=self.img_title,
            dest=from_v2.lerp(to_v2, ratio)
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self.callback()

    def _img_band(self) -> Surface:
        img = Surface(size=(WX, _BAND_H), flags=SRCALPHA)
        rect_fill(color="white", rect=Rect(0, 0, WX, _BAND_H), surface=img)
        return img

    def _img_title(self) -> Surface:
        return MS_MINCHO_COL(self.board_view.board.turn_player.name, _FONT_H, "black")

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT

    def _title_y(self) -> int:
        return int(WY/2-self.img_title.get_height()/2)

    def _left_v2(self) -> V2:
        return V2(-self.img_title.get_width(), self._title_y())

    def _center_v2(self) -> V2:
        return V2(WX/2-self.img_title.get_width()/2, self._title_y())

    def _right(self) -> V2:
        return V2(WX, self._title_y())
