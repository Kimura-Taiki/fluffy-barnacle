import pygame
from typing import Callable
from functools import partial

from mod.const import MS_MINCHO_32PT, screen, IMG_GOTTENON_BG
from mod.youso import Youso
from mod.core_view import CoreView

class Gottenon(Youso):
    def __init__(self, core_view: CoreView, text: str, x: int, y: int, **kwargs: Callable[..., None]) -> None:
        super().__init__(x=x, y=y, draw=self._draw_gottenon_off, **kwargs)
        self.text = text
        self.img_text = MS_MINCHO_32PT(self.text)
        self.core_view: CoreView = core_view

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.x, self.y
        if cx-140 < mx and mx < cx+140 and cy-30 < my and my < cy+30:
            return True
        return False

    def on(self) -> None:
        self.draw = partial(self._draw_gottenon_on, self)

    def off(self) -> None:
        self.draw = partial(self._draw_gottenon_off, self)

    @staticmethod
    def _draw_gottenon_off(gottenon: 'Gottenon') -> None:
        IMG_GOTTENON_BG.set_alpha(64)
        screen.blit(source=IMG_GOTTENON_BG, dest=gottenon.topleft(source=IMG_GOTTENON_BG))
        IMG_GOTTENON_BG.set_alpha(255)
        gottenon.img_text.set_alpha(128)
        screen.blit(source=gottenon.img_text, dest=gottenon.topleft(source=gottenon.img_text))
        gottenon.img_text.set_alpha(255)

    @staticmethod
    def _draw_gottenon_on(gottenon: 'Gottenon') -> None:
        IMG_GOTTENON_BG.set_alpha(255)
        screen.blit(source=IMG_GOTTENON_BG, dest=gottenon.topleft(source=IMG_GOTTENON_BG))
        gottenon.img_text.set_alpha(255)
        screen.blit(source=gottenon.img_text, dest=gottenon.topleft(source=gottenon.img_text))
