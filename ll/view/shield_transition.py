from pygame import Surface, Vector2 as V2, transform

from any.pictures import IMG_SHIELD
from any.screen import WV2, FRAMES_PER_SECOND
from any.timer_functions import frames
from model.ui_element import UIElement

_SECONDS = 0.5
_WAIT = int(FRAMES_PER_SECOND*_SECONDS)

from ptc.transition import Transition
class ShieldTransition():
    def __init__(self, to_v2: V2, canvas: Surface) -> None:
        self.from_v2 = WV2/2
        self.to_v2 = to_v2
        self._drawing_in_progress = True
        self.frames = frames()
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

    def in_progress(self) -> bool:
        return self._drawing_in_progress
    
    def _img_rz(self) -> Surface:
        IMG_SHIELD.set_alpha(int(64+191*self._ratio()))
        img = transform.rotozoom(
            surface=IMG_SHIELD,
            angle=0.0,
            scale=2.0-self._ratio()
        )
        IMG_SHIELD.set_alpha(255)
        return img

    def _ratio(self) -> float:
        return (frames()-self.frames)/_WAIT

    def _complete(self) -> None:
        self._drawing_in_progress = False
