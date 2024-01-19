import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable
from functools import partial

from mod.const import GAINSBORO, BLACK, MS_MINCHO_32PT, screen, IMG_GOTTENON_BG
from mod.youso import Youso

class Gottenon(Youso):
    def __init__(self, text: str, x: int, y: int, **kwargs) -> None:
        super().__init__(x=x, y=y, draw=self._draw_gottenon_off, **kwargs)
        self.text = text
        self.img_text = MS_MINCHO_32PT(self.text)

    def on(self) -> None:
        self.draw = partial(self._draw_gottenon_on, self)

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
