import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, BRIGHT, WX, WY, draw_aiharasuu
from mod.ol.over_layer import OverLayer
from mod.huda import Huda, default_draw
from mod.ol.view_banmen import view_youso
from mod.card import Card, auto_di, Kougeki
from mod.taba import Taba
from mod.tf.taba_factory import TabaFactory
from mod.controller import controller

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
SCALE_SIZE = 150

_aura_damage = Card(img=IMG_AURA_DAMAGE, name="", cond=auto_di)
_life_damage = Card(img=IMG_LIFE_DAMAGE, name="", cond=auto_di)

class PlayKougeki():
    def __init__(self, huda: Huda) -> None:
        if not isinstance(huda.card, Kougeki):
            raise ValueError(f"Invalid huda.card: {type(huda.card)}")
        self.kougeki = huda.card
        self.name = f"攻撃:{huda.card.name}の使用"
        self.source_huda = huda
        self.inject_func = huda.delivery.inject_view
        self.delivery = huda.delivery
        self.taiou_taba: Taba = []
        self.uke_taba: Taba = []

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()
        if aura_huda := next((huda for huda in self.uke_taba if huda.card == _aura_damage), None):
            draw_aiharasuu(surface=screen, dest=aura_huda.dest-Vector2(SCALE_SIZE, SCALE_SIZE)/2,
                           num=self.kougeki.aura_damage(self.delivery, self.source_huda.hoyuusya),
                           size=SCALE_SIZE)
        if life_huda := next((huda for huda in self.uke_taba if huda.card == _life_damage), None):
            draw_aiharasuu(surface=screen, dest=life_huda.dest-Vector2(SCALE_SIZE, SCALE_SIZE)/2,
                           num=self.kougeki.life_damage(self.delivery, self.source_huda.hoyuusya),
                           size=SCALE_SIZE)

    def get_hover(self) -> Any | None:
        return view_youso

    def open(self) -> None:
        bac = TabaFactory(inject_kwargs={
            "draw": self._draw, "hover": Huda.detail_draw, "mousedown": self._mousedown, "mouseup": self._mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        self.uke_taba = bac.maid_by_cards(cards=[_aura_damage, _life_damage], hoyuusya=self.source_huda.hoyuusya)

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

    def _draw(self, huda: Huda) -> None:
        if controller.hover == huda:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
            screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
        else:
            default_draw(huda=huda)

    def _mousedown(self, huda: Huda) -> None:
        ...

    def _mouseup(self, huda: Huda) -> None:
        ...


# compatible_with(, OverLayer)
