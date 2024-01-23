from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import screen, draw_aiharasuu
from mod.youso import Youso

class Utuwa(Youso):
    def __init__(self, img: Surface, is_own: bool, num: int, x: int | float = 0, y: int | float = 0,
                 **kwargs: Callable[..., None]) -> None:
        super().__init__(x=x, y=y, **kwargs)
        self.img = img
        self.is_own = is_own
        self.num = num
        self.draw = partial(self._draw)

    def _draw(self) -> None:
        screen.blit(source=self.img, dest=[self.x, self.y])
        draw_aiharasuu(surface=screen, dest=(self.x, self.y), num=self.num)
