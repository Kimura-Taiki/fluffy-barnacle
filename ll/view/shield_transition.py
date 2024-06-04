from pygame import Surface, Vector2 as V2, transform

from any.func import make_progress_funcs
from any.pictures import IMG_SHIELD
from any.screen import WV2
from any.timer_functions import make_ratio_func
from model.ui_element import UIElement

_SECONDS = 0.5

from ptc.transition import Transition
class ShieldTransition():
    def __init__(self, to_v2: V2, canvas: Surface) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self._ratio = make_ratio_func(seconds=_SECONDS)
        self.from_v2 = WV2/2
        self.to_v2 = to_v2
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return None

    def draw(self) -> None:
        img_rz = self._img_rz()
        self.canvas.blit(
            source=img_rz,
            dest=self.from_v2.lerp(self.to_v2, self._ratio())-V2(img_rz.get_size())/2
        )

    def elapse(self) -> None:
        if self._ratio() >= 1:
            self._complete()

    def _img_rz(self) -> Surface:
        IMG_SHIELD.set_alpha(int(64+191*self._ratio()))
        img = transform.rotozoom(
            surface=IMG_SHIELD,
            angle=0.0,
            scale=2.0-self._ratio()
        )
        IMG_SHIELD.set_alpha(255)
        return img
