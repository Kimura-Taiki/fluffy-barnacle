import pygame
from typing import Callable
from functools import partial

from mod.const import MS_MINCHO_32PT, screen, IMG_GOTTENON_BG, WX, WY
from mod.youso import Youso
from mod.core_view import CoreView

def joined_commands(commands: list[Callable[[], None]]) -> Callable[[], None]:
    def mono_command() -> None:
        for command in commands:
            command()
    return mono_command

class Gottenon(Youso):
    def __init__(self, core_view: CoreView, name: str, x: int, y: int, **kwargs: Callable[..., None]) -> None:
        print(core_view.is_own)
        if core_view.is_own == False:
            x, y = WX-x, WY-y
        super().__init__(x=x, y=y, draw=self._draw_gottenon_off, **kwargs)
        self.name = name
        self.core_view: CoreView = core_view
        self.redraw_img_text()

    def redraw_img_text(self) -> None:
        self.img_text = MS_MINCHO_32PT(self.core_view.text(name=self.name))

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
        IMG_GOTTENON_BG.set_alpha(128)
        screen.blit(source=IMG_GOTTENON_BG, dest=gottenon.topleft(source=IMG_GOTTENON_BG))
        IMG_GOTTENON_BG.set_alpha(255)
        gottenon.img_text.set_alpha(192)
        screen.blit(source=gottenon.img_text, dest=gottenon.topleft(source=gottenon.img_text))
        gottenon.img_text.set_alpha(255)

    @staticmethod
    def _draw_gottenon_on(gottenon: 'Gottenon') -> None:
        IMG_GOTTENON_BG.set_alpha(255)
        screen.blit(source=IMG_GOTTENON_BG, dest=gottenon.topleft(source=IMG_GOTTENON_BG))
        gottenon.img_text.set_alpha(255)
        screen.blit(source=gottenon.img_text, dest=gottenon.topleft(source=gottenon.img_text))
