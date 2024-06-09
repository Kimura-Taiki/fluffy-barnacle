from pygame import Surface, Vector2 as V2

from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.transition import Transition
class StaticTransition():
    def __init__(
            self, img_actor: Surface, center: V2, canvas: Surface,
            seconds: float=_SECONDS
    ) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_actor = img_actor
        self.topleft = center-V2(img_actor.get_size())/2
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.canvas.blit(source=self.img_actor, dest=self.topleft)
