import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable
from functools import partial

from mod.const import screen, draw_aiharasuu, WX, WY, KAMITE
from mod.youso import Youso

class Utuwa(Youso):
    def __init__(self, img: Surface, hoyuusya: int, osame: int, x: int | float = 0, y: int | float = 0, max: int=99,
                 draw: Callable[[], None] | None=None, **kwargs: Callable[..., None]) -> None:
        if hoyuusya == KAMITE:
            x, y = WX-x, WY-y
        super().__init__(x=x, y=y, **kwargs)
        self.img = img
        self.hoyuusya = hoyuusya
        self.osame = osame
        self.max = max
        self.draw = draw if draw else lambda: self._draw()

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        [hx, hy] = Vector2(self.img.get_size())/2
        return self.x-hx <= mx and mx <= self.x+hx and self.y-hy <= my and my <= self.y+hy

    def _draw(self) -> None:
        screen.blit(source=self.img, dest=-Vector2(self.img.get_size())/2+[self.x, self.y])
        draw_aiharasuu(surface=screen, dest=-Vector2(self.img.get_size())/2+(self.x, self.y), num=self.osame)

    def isyuku_draw(self) -> None:
        screen.blit(source=self.img, dest=-Vector2(self.img.get_size())/2+[self.x, self.y])
