from pygame import Surface, Vector2 as V2

from any.pictures import IMG_CHAIN_L, IMG_CHAIN_R
from view.progress_helper import ProgressHelper

_SECONDS = 0.5
_CV2 = V2(340, 270)

from ptc.transition import Transition
class BindTransition():
    def __init__(
            self, img_actor: Surface, center: V2, canvas: Surface, seconds: float=_SECONDS
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
        self.canvas.blit(source=self._img(), dest=self.topleft)

    def _img(self) -> Surface:
        img = self.img_actor.copy()
        params: list[tuple[Surface, V2, V2]] = [
            (IMG_CHAIN_L, -_CV2, V2()),
            (IMG_CHAIN_R, V2(_CV2.x, -_CV2.y), V2()),
            (IMG_CHAIN_L, -_CV2+V2(0, 475-_CV2.y), V2(0, 475-_CV2.y)),
            (IMG_CHAIN_R, V2(_CV2.x, -_CV2.y)+V2(0, 475-_CV2.y), V2(0, 475-_CV2.y)),
        ]
        for source, from_v2, to_v2 in params:
            img.blit(
                source=source,
                dest=from_v2.lerp(to_v2, self._ratio())
            )
        return img