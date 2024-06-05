from pygame import Surface, Vector2 as V2

from any.pictures import IMG_BRIGHT
from any.screen import screen, WX, WY
from model.kard import Kard
from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.view import View
class UseKardView():
    def __init__(self, view: View, kard: Kard) -> None:
        self._ratio, self.in_progress, _, _, self.get_hover, self.elapse\
            = ProgressHelper(seconds=_SECONDS).provide_progress_funcs()
        self.board_view = view
        self.kard = kard
        self.img_kard = kard.picture()

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(
            source=self._img_bright_kard(),
            dest=V2(WX, WY)/2-V2(self.img_kard.get_size())/2
        )

    def _img_bright_kard(self) -> Surface:
        img = Surface(size=self.img_kard.get_size())
        img.blit(source=self.img_kard, dest=(0, 0))
        img.blit(source=IMG_BRIGHT, dest=(0, self._shift_y()))
        return img

    def _shift_y(self) -> int:
        h = self.img_kard.get_height()
        return int(-12-h+2*h*self._ratio())
