import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, pass_func, screen
from mod.youso import Youso
from mod.router import controller
from mod.popup_message import popup_message

class Button(Youso):
    def __init__(self, img_nega: Surface, img_lighten: Surface, x: int | float | None=None, y: int | float | None=None,
                 mouseup: Callable[[Youso], None]=pass_func) -> None:
        self.img_nega = img_nega
        self.img_lighten = img_lighten
        super().__init__(
            x if x is not None else WX-self.img_nega.get_width()/2,
            y if y is not None else WY-self.img_nega.get_height()/2,
            draw=Button._draw, mousedown=Button._mousedown, mouseup=mouseup)

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        [hx, hy] = Vector2(self.img_nega.get_size())/2
        return self.x-hx <= mx and mx <= self.x+hx and self.y-hy <= my and my <= self.y+hy

    def _draw(self) -> None:
        screen.blit(source=self.img_lighten if controller.hover == self else self.img_nega,
                    dest=self.dest-Vector2(self.img_lighten.get_size())/2)

    def _mousedown(self) -> None:
        controller.active = self
        # popup_message.add(text="ボタンを押したよ")
