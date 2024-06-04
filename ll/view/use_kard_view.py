from pygame import Surface, Vector2 as V2

from any.func import make_progress_funcs
from any.pictures import IMG_BRIGHT
from any.screen import screen, WX, WY
from any.timer_functions import make_ratio_func
from model.kard import Kard
from model.ui_element import UIElement

_SECONDS = 0.5

from ptc.view import View
class UseKardView():
    def __init__(self, view: View, kard: Kard) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=_SECONDS)
        self.board_view = view
        self.kard = kard
        self.img_kard = kard.picture()
        self.ui_element = UIElement(mousedown=self._complete)

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(
            source=self._img_bright_kard(),
            dest=V2(WX, WY)/2-V2(self.img_kard.get_size())/2
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def _img_bright_kard(self) -> Surface:
        img = Surface(size=self.img_kard.get_size())
        img.blit(source=self.img_kard, dest=(0, 0))
        img.blit(source=IMG_BRIGHT, dest=(0, self._shift_y()))
        return img

    def _shift_y(self) -> int:
        h = self.img_kard.get_height()
        return int(-12-h+2*h*self._ratio())
