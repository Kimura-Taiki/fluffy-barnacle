import pygame
from typing import Any

from mod.ol.over_layer import OverLayer
from mod.huda import Huda
from mod.const import screen, IMG_GRAY_LAYER, compatible_with
from mod.ol.undo_mouse import make_undo_youso
from mod.ol.view_banmen import view_youso

_gray_youso = make_undo_youso(text="PlayKougeki")

class PlayKougeki():
    def __init__(self, huda: Huda) -> None:
        self.name = "攻撃の使用"
        self.source_huda = huda
        self.inject_func = huda.delivery.inject_view
        self.delivery = huda.delivery

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])

    def get_hover(self) -> Any | None:
        return view_youso

    def open(self) -> None:
        ...

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

compatible_with(PlayKougeki(Huda(img=pygame.Surface((16, 16)))), OverLayer)
