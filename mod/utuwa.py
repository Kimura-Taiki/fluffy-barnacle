from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import screen, draw_aiharasuu, WX, WY
from mod.youso import Youso

class Utuwa(Youso):
    def __init__(self, img: Surface, is_own: bool, num: int, x: int | float = 0, y: int | float = 0,
                 **kwargs: Callable[..., None]) -> None:
        if is_own == False:
            x, y = WX-x, WY-y
        super().__init__(x=x, y=y, **kwargs)
        self.img = img
        self.is_own = is_own
        self.num = num
        self.draw = partial(self._draw)

    def _draw(self) -> None:
        screen.blit(source=self.img, dest=[self.x-30, self.y-30])
        draw_aiharasuu(surface=screen, dest=(self.x-30, self.y-30), num=self.num)
