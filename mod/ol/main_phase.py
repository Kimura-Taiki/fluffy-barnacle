import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable

from mod.const import compatible_with, pass_func, screen, IMG_ZYOGAI_AREA, WX, WY, WHITE
from mod.ol.over_layer import OverLayer
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.delivery import Delivery, duck_delivery
from mod.controller import controller

class Button(Youso):
    def __init__(self, img: Surface, x: int | float = 0, y: int | float = 0) -> None:
        super().__init__(x, y, draw=Button._draw, mousedown=Button._mousedown)
        self.img = img

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        [hx, hy] = Vector2(self.img.get_size())/2
        return self.x-hx <= mx and mx <= self.x+hx and self.y-hy <= my and my <= self.y+hy

    def _draw(self) -> None:
        if controller.hover == self:
            sx, sy = self.img.get_size()
            screen.fill(color=WHITE, rect=[self.x-sx/2, self.y-sy/2, sx, sy])
            self.img.set_alpha(192)
            screen.blit(source=self.img, dest=self.dest-Vector2(self.img.get_size())/2)
            self.img.set_alpha(255)
        else:
            screen.blit(source=self.img, dest=self.dest-Vector2(self.img.get_size())/2)

    def _mousedown(self) -> None:
        controller.active = self
        popup_message.add(text="ボタンを押したよ")

class MainPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "メインフェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.button = Button(img=IMG_ZYOGAI_AREA, x=WX/2, y=WY/2)

    def elapse(self) -> None:
        self.button.draw()

    def get_hover(self) -> Youso | None:
        return self.button if self.button.is_cursor_on() else None

    def open(self) -> None:
        ...

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

compatible_with(MainPhase(), OverLayer)