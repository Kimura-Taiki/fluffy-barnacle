from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect, img_zoom, dest_rect_center
from any.pictures import IMG_BACK
from model.kard import Kard
from model.ui_element import UIElement
from view.progress_helper import ProgressHelper

_RATIO = V2(340, 475)
_SECONDS = 0.5

from ptc.transition import Transition
class PeepTransition():
    def __init__(
            self, rect: Rect, kard: Kard, canvas: Surface) -> None:
        self._ratio, _, _, _, _, self.elapse\
            = ProgressHelper(seconds=_SECONDS).provide_progress_funcs()
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self.canvas = canvas
        self.img_back = img_zoom(img=IMG_BACK, rect=self.rect, ratio=_RATIO)
        self.img_front = img_zoom(
            img=kard.picture(),
            rect=self.rect,
            ratio=_RATIO
        )
        self._clicked = False
        self._ui_element = UIElement(mousedown=self._complete)

    def get_hover(self) -> UIElement | None:
        return self._ui_element

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.offset_draw()

    def offset_draw(self, offset: V2=V2(0, 0)) -> None:
        img = self.img_open()
        self.canvas.blit(
            source=img,
            dest=dest_rect_center(rect=self.rect, img=img)+offset
        )

    def in_progress(self) -> bool:
        return not self._clicked

    def img_open(self) -> Surface:
        img, sx = (self.img_back, self.img_back.get_width()*(0.5-f)/0.5)\
            if (f := self._ratio()) < 0.5 else\
                (self.img_front, self.img_back.get_width()*(f-0.5)/0.5)
        return transform.smoothscale(surface=img, size=(sx, IMG_BACK.get_height()))

    def _complete(self) -> None:
        if self._ratio() >= 1:
            self._clicked = True