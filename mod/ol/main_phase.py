import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import compatible_with, pass_func, screen, WX, WY, IMG_TURN_END, IMG_TURN_END_LIGHTEN
from mod.ol.over_layer import OverLayer
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.delivery import Delivery, duck_delivery
from mod.controller import controller
from mod.moderator import moderator

class Button(Youso):
    def __init__(self, x: int | float = WX-30, y: int | float = WY-60, mouseup: Callable[[Youso], None]=pass_func) -> None:
        super().__init__(x, y, draw=Button._draw, mousedown=Button._mousedown, mouseup=mouseup)
        self.img_nega = pygame.transform.scale(surface=IMG_TURN_END, size=Vector2(IMG_TURN_END.get_size())*2)
        self.x = WX-self.img_nega.get_width()/2
        self.y = WY-self.img_nega.get_height()/2
        self.img_lighten = pygame.transform.scale(surface=IMG_TURN_END_LIGHTEN, size=Vector2(IMG_TURN_END_LIGHTEN.get_size())*2)

    def is_cursor_on(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        [hx, hy] = Vector2(self.img_nega.get_size())/2
        return self.x-hx <= mx and mx <= self.x+hx and self.y-hy <= my and my <= self.y+hy

    def _draw(self) -> None:
        if controller.hover == self:
            sx, sy = self.img_nega.get_size()
            screen.blit(source=self.img_lighten, dest=self.dest-Vector2(self.img_lighten.get_size())/2)
        else:
            screen.blit(source=self.img_nega, dest=self.dest-Vector2(self.img_nega.get_size())/2)

    def _mousedown(self) -> None:
        controller.active = self
        popup_message.add(text="ボタンを押したよ")

class MainPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "メインフェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.button = Button(mouseup=self._mouseup_turn_end)

    def elapse(self) -> None:
        self.button.draw()

    def get_hover(self) -> Youso | None:
        return self.button if self.button.is_cursor_on() else None

    def open(self) -> None:
        ...

    def close(self) -> int:
        popup_message.add(text="ターンを終了します")
        return 0

    def moderate(self, stat: int) -> None:
        ...

    def _mouseup_turn_end(self, youso: Youso) -> None:
        moderator.pop()        

compatible_with(MainPhase(), OverLayer)