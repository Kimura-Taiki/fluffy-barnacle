from pygame import Surface, Vector2 as V2, transform, math

from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.transition import Transition
class ZoomTransitions():
    def __init__(
            self, img_actor: Surface, center: V2, from_scale: float,
            to_scale: float, canvas: Surface, seconds: float=_SECONDS
    ) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_actor = img_actor
        self.canvas = canvas
        self.center = center
        self.from_scale = from_scale
        self.to_scale = to_scale

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        img = transform.rotozoom(
            surface=self.img_actor,
            angle=0.0,
            scale=math.lerp(self.from_scale, self.to_scale, self._ratio())
        )
        self.canvas.blit(source=img, dest=self.center-V2(img.get_size())/2)
