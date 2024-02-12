from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable
from functools import partial

from mod.const import screen, draw_aiharasuu, WX, WY, KAMITE
from mod.youso import Youso

class Utuwa(Youso):
    def __init__(self, img: Surface, hoyuusya: int, num: int, x: int | float = 0, y: int | float = 0, max: int=99,
                 **kwargs: Callable[..., None]) -> None:
        if hoyuusya == KAMITE:
            x, y = WX-x, WY-y
        super().__init__(x=x, y=y, **kwargs)
        self.img = img
        self.hoyuusya = hoyuusya
        self.osame = num
        self.max = max
        self.draw = partial(self._draw)

    def _draw(self) -> None:
        screen.blit(source=self.img, dest=-Vector2(self.img.get_size())/2+[self.x, self.y])
        draw_aiharasuu(surface=screen, dest=-Vector2(self.img.get_size())/2+(self.x, self.y), num=self.num)

    def isyuku_draw(self) -> None:
        screen.blit(source=self.img, dest=-Vector2(self.img.get_size())/2+[self.x, self.y])

    @property
    def num(self) -> int:
        return self.osame
    
    @num.setter
    def num(self, value: int) -> None:
        self.osame = value
