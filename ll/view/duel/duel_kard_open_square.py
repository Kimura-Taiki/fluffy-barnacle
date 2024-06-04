from pygame import Surface, Vector2 as V2, transform, Rect

# from any.func import ratio_rect, img_zoom, dest_rect_center, make_progress_funcs
from any.func import ratio_rect, img_zoom, dest_rect_center
from any.pictures import IMG_BACK
from any.timer_functions import make_ratio_func
from model.kard import Kard
from model.ui_element import UIElement

_RATIO = V2(340, 475)

from typing import Callable
def make_progress_funcs(ratio: Callable[[], float]=lambda: 0.0) -> tuple[
    Callable[[], bool], Callable[[], None], UIElement,
    Callable[[], UIElement | None], Callable[[], None]
]:
    '''
    in_progress関数, _complete命令, ui_element属性, get_hover関数, elapse命令の
    メソッド五種を一括して作成します。
    不要なメソッドの項目には「_」を指定してください。戻り値を5つ全て取らないとエラーです。
    '''
    in_drawing_progress = True
    def in_progress() -> bool:
        nonlocal in_drawing_progress
        return in_drawing_progress
    def _complete() -> None:
        nonlocal in_drawing_progress
        in_drawing_progress = False
    ui_element = UIElement(mousedown=_complete)
    def get_hover() -> UIElement | None:
        return ui_element
    def elapse() -> None:
        if ratio() >= 1.0:
            _complete()
    return in_progress, _complete, ui_element, get_hover, elapse


from ptc.transition import Transition
class DuelKardOpenSquare():
    def __init__(
            self, rect: Rect, kard: Kard, canvas: Surface, seconds: float=0.0
        ) -> None:
        self.in_progress, self._complete, self.get_hover, _, self.elapse = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=seconds) if seconds else lambda: 0.0
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.kard = kard
        self.canvas = canvas
        self.img_back = img_zoom(img=IMG_BACK, rect=self.rect, ratio=_RATIO)
        self.img_front = img_zoom(
            img=kard.picture(),
            rect=self.rect,
            ratio=_RATIO
        )

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

    def img_open(self) -> Surface:
        img, sx = (self.img_back, self.img_back.get_width()*(0.5-f)/0.5)\
            if (f := self._ratio()) < 0.5 else\
                (self.img_front, self.img_back.get_width()*(f-0.5)/0.5)
        return transform.smoothscale(surface=img, size=(sx, IMG_BACK.get_height()))
