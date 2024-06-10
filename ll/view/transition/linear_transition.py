from pygame import Surface, Vector2 as V2

from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.transition import Transition
class LinearTransition():
    def __init__(self, img_actor: Surface, from_v2: V2, to_v2: V2, canvas: Surface, seconds: float=_SECONDS) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_actor = img_actor
        self.from_v2 = from_v2
        self.to_v2 = to_v2
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.canvas.blit(
            source=self.img_actor,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())-V2(self.img_actor.get_size())/2
        )
