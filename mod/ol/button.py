import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, pass_func, screen
from mod.youso import Youso
from mod.controller import controller
from mod.popup_message import popup_message

class Button(Youso):
    def __init__(self, img_nega: Surface, img_lighten: Surface, x: int | None=None, y: int | None=None,
                 mouseup: Callable[[Youso], None]=pass_func) -> None:
        super().__init__(x, y, draw=Button._draw, mousedown=Button._mousedown, mouseup=mouseup)
        self.img_nega = img_nega
        self.x = x if x is not None else WX-self.img_nega.get_width()/2
        self.y = y if y is not None else WY-self.img_nega.get_height()/2
        self.img_lighten = img_lighten

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        [hx, hy] = Vector2(self.img_nega.get_size())/2
        return self.x-hx <= mx and mx <= self.x+hx and self.y-hy <= my and my <= self.y+hy

    def _draw(self) -> None:
        screen.blit(source=self.img_lighten if controller.hover == self else self.img_nega,
                    dest=self.dest-Vector2(self.img_lighten.get_size())/2)

    def _mousedown(self) -> None:
        controller.active = self
        popup_message.add(text="ボタンを押したよ")
