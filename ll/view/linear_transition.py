from pygame import Surface, Vector2 as V2

from any.screen import FRAMES_PER_SECOND
from any.timer_functions import frames
from model.ui_element import UIElement

_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class LinearTransition():
    def __init__(self, img_actor: Surface, from_v2: V2, to_v2: V2, canvas: Surface) -> None:
        self.img_actor = img_actor
        self.from_v2 = from_v2
        self.to_v2 = to_v2
        self._drawing_in_progress = True
        self.frames = frames()
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        self.canvas.blit(
            source=self.img_actor,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())-V2(self.img_actor.get_size())/2
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