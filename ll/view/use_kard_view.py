from pygame import Surface, Vector2 as V2
from typing import Callable

from any.pictures import IMG_BRIGHT
from any.screen import screen, WX, WY, FRAMES_PER_SECOND
from any.timer_functions import frames
from model.kard import Kard
from model.ui_element import UIElement

_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.view import View
class UseKardView():
    def __init__(self, view: View, kard: Kard, callback: Callable[..., None]) -> None:
        self.board_view = view
        self.kard = kard
        self.img_kard = kard.picture()
        self.callback = callback
        self.frames = frames()
        self.ui_element = UIElement(mousedown=self.callback)

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
            self.callback()

    def _img_bright_kard(self) -> Surface:
        img = Surface(size=self.img_kard.get_size())
        img.blit(source=self.img_kard, dest=(0, 0))
        img.blit(source=IMG_BRIGHT, dest=(0, self._shift_y()))
        return img

    def _shift_y(self) -> int:
        h = self.img_kard.get_height()
        return int(-12-h+2*h*self._ratio())

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT