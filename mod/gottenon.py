from pygame.surface import Surface
from pygame.math import Vector2

from mod.const import GAINSBORO, MS_MINCHO_32PT, screen
from mod.youso import Youso

class Gottenon(Youso):
    def __init__(self, text: str, x: int, y: int, **kwargs) -> None:
        super().__init__(x=x, y=y, draw=self._draw_gottenon, **kwargs)
        self.img_bg = Surface((280, 60))
        self.img_bg.fill(GAINSBORO)
        self.text = text
        self.img_text = MS_MINCHO_32PT(self.text)

    @staticmethod
    def _draw_gottenon(gottenon: 'Gottenon') -> None:
        gottenon.img_bg.set_alpha(255)
        screen.blit(source=gottenon.img_bg, dest=gottenon.topleft(source=gottenon.img_bg))
        screen.blit(source=gottenon.img_text, dest=gottenon.topleft(source=gottenon.img_text))
