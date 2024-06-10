from pygame import Surface, Vector2 as V2, SRCALPHA

from any.screen import screen
from view.progress_helper import ProgressHelper

_SECONDS = 0.5

from ptc.transition import Transition
class SlashTransition():
    def __init__(
            self, img_actor: Surface, center: V2,
            canvas: Surface=screen, seconds: float=_SECONDS
    ) -> None:
        self._ratio, self.in_progress, _, _, _, self.elapse\
            = ProgressHelper(seconds=seconds).provide_progress_funcs()
        self.get_hover = ProgressHelper.empty_get_hover
        self.img_actor = img_actor
        self._size = V2(img_actor.get_width()/2, img_actor.get_height())
        self.img_left = self._img_left()
        self.left_tl = center-self._size/2
        self.img_right = self._img_right()
        self.right_tl = center-self._size/2+V2(self._size.x, 0)
        self.canvas = canvas

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        self.img_left.set_alpha(int(255-255*self._ratio()))
        self.img_right.set_alpha(int(255-255*self._ratio()))
        dv2 = V2(0, self._size.y*self._ratio())
        self.canvas.blit(source=self.img_left, dest=self.left_tl-dv2)
        self.canvas.blit(source=self.img_right, dest=self.right_tl+dv2)

    def _img_left(self) -> Surface:
        img = Surface((self._size), SRCALPHA)
        img.blit(source=self.img_actor, dest=(0, 0), area=((0, 0), self._size))
        return img
    
    def _img_right(self) -> Surface:
        img = Surface((self._size), SRCALPHA)
        img.blit(source=self.img_actor, dest=(0, 0), area=((self._size.x, 0), self._size))
        return img
