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
from mod.ol.button import Button

class MainPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "メインフェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.button = Button(img_nega=IMG_TURN_END, img_lighten=IMG_TURN_END_LIGHTEN, mouseup=self._mouseup_turn_end)

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