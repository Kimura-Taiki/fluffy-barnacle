from pygame import Surface, Vector2 as V2

from any.font import MS_MINCHO_COL
from any.screen import screen, WX, WY, FRAMES_PER_SECOND
from any.timer_functions import frames
from model.ui_element import UIElement

_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.view import View
class LinearView():
    def __init__(self, view: View, img_back: Surface, from_v2: V2, to_v2: V2) -> None:
        self.board_view = view
        self.img_back = img_back
        self.from_v2 = from_v2
        self.to_v2 = to_v2
        self._drawing_in_progress = True
        self.frames = frames()
        self.ui_element = UIElement(mousedown=self._complete)

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(
            source=MS_MINCHO_COL("in drawing...", 64, "black"),
            dest=(WX/2-112, WY/2-32)
        )
        screen.blit(
            source=self.img_back,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())-V2(self.img_back.get_size())/2
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def in_progress(self) -> bool:
        return self._drawing_in_progress

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT
    
    def _complete(self) -> None:
        self._drawing_in_progress = False