from pygame import Surface, Vector2 as V2, transform

from any.pictures import IMG_BACK
from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.transition import Transition
class FaceUpTransition():
    def __init__(
            self, img_after: Surface, center: V2, canvas: Surface,
            img_before: Surface=IMG_BACK, seconds: float=_SECONDS
    ) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_after = img_after
        self.center = center
        self.canvas = canvas
        self.img_before = img_before

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        img = transform.smoothscale(
            surface=self.img_before if self._ratio() < 0.5 else self.img_after,
            size=(
                IMG_BACK.get_width()*abs(0.5-self._ratio())/0.5,
                IMG_BACK.get_height()
            )
        )
        self.canvas.blit(source=img, dest=self.center-V2(img.get_size())/2)
