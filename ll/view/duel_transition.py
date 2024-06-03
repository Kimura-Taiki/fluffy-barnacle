from pygame import Surface, Vector2 as V2, transform, Rect

from any.func import ratio_rect
from any.pictures import IMG_DUEL, IMG_BACK
from any.screen import FRAMES_PER_SECOND
from any.timer_functions import frames
from model.ui_element import UIElement

_RATIO = V2(880, 475)
_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class DuelTransition():
    def __init__(self, rect: Rect, canvas: Surface) -> None:
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self._drawing_in_progress = True
        self.frames = frames()
        self.canvas = canvas
        self.img_back = self._img_zoom(img=IMG_BACK)
        self.img_duel = self._img_zoom(img=IMG_DUEL)
        self.ui_element = UIElement(mousedown=self._complete)

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def draw(self) -> None:
        self.canvas.blit(source=self.img_back, dest=self._dest_left())
        self.canvas.blit(source=self.img_back, dest=self._dest_right())
        img_rz = self._img_rz()
        self.canvas.blit(
            source=img_rz,
            dest=V2(self.rect.center)-V2(img_rz.get_size())/2
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def in_progress(self) -> bool:
        return self._drawing_in_progress

    def _img_zoom(self, img: Surface) -> Surface:
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/_RATIO.x)

    def _dest_left(self) -> V2:
        from_v2 = V2(self.rect.topleft)-V2(self.img_back.get_width(), 0)
        to_v2 = V2(self.rect.topleft)
        return from_v2.lerp(to_v2, self._ratio())

    def _dest_right(self) -> V2:
        from_v2 = V2(self.rect.topright)
        to_v2 = V2(self.rect.topright)-V2(self.img_back.get_width(), 0)
        return from_v2.lerp(to_v2, self._ratio())
    
    def _img_rz(self) -> Surface:
        return transform.rotozoom(
            surface=self.img_duel,
            angle=0.0,
            scale=3.0-self._ratio()*2
        )

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT

    def _complete(self) -> None:
        self._drawing_in_progress = False
