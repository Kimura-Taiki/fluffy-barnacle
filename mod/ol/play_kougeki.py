import pygame
from typing import Any, Callable

from mod.ol.over_layer import OverLayer
from mod.huda import Huda
from mod.const import screen, IMG_GRAY_LAYER, compatible_with
from mod.popup_message import popup_message
from mod.controller import controller
from mod.moderator import moderator
from mod.youso import Youso

def _mousedown(huda: Huda) -> None:
    popup_message.add(text="PlayKougeki.mousedown でクリックしたよ")
    controller.active = huda

def _mouseup(huda: Huda) -> None:
    moderator.pop()

_gray_youso = Youso(mousedown=_mousedown, mouseup=_mouseup)

class PlayKougeki():
    def __init__(self, huda: Huda) -> None:
        self.name = "攻撃の使用"
        self.source_huda = huda
        self.inject_func = huda.delivery.inject_view
        self.delivery = huda.delivery

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])

    def get_hover(self) -> Any | None:
        return _gray_youso

    def open(self) -> None:
        ...

    def close(self) -> int:
        ...

    def moderate(self, stat: int) -> None:
        ...

compatible_with(PlayKougeki(Huda(img=pygame.Surface((16, 16)))), OverLayer)
