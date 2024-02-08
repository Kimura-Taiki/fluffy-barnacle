#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, BRIGHT, WX, WY, draw_aiharasuu\
    , TC_SUTEHUDA, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, opponent, POP_TAIOUED
from mod.ol.over_layer import OverLayer
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card, auto_di, Kougeki, SuuziDI, Damage
from mod.taba import Taba
from mod.tf.taba_factory import TabaFactory
from mod.controller import controller
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_UX: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_UY: Callable[[int, int], float] = lambda i, j: WY-150
SCALE_SIZE = 180

class PlayTaiou():
    name = "対応時にstat戻り値を与える為の空OverLayer"

    def __init__(self, huda: Huda) -> None:
        self.huda = huda
        self.delivery = huda.delivery
        self.inject_func = huda.delivery.inject_view

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.huda.card.kaiketu(delivery=self.huda.delivery, hoyuusya=self.huda.hoyuusya, huda=self.huda)
        moderator.pop()

    def close(self) -> Any:
        print("PopTaioued")
        return POP_TAIOUED, self.huda

    def moderate(self, stat: int) -> None:
        ...

# compatible_with(, OverLayer)
