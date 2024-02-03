#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, BRIGHT, WX, WY, draw_aiharasuu\
    , TC_SUTEHUDA, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR
from mod.ol.over_layer import OverLayer
from mod.huda import Huda, available_draw
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
SCALE_SIZE = 180

class Choice():
    def __init__(self, kougeki: Kougeki, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.kougeki = kougeki
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"攻撃:{kougeki.name}の使用"
        self.inject_func = delivery.inject_view
        self.taiou_taba: Taba = Taba()
        self.uke_taba: Taba = Taba()

    def elapse(self) -> None:
        screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.uke_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        bac = TabaFactory(inject_kwargs={
            "draw": available_draw, "hover": Huda.detail_draw, "mousedown": self._mousedown, "mouseup": self._mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        _ad_card = Damage(img=IMG_AURA_DAMAGE, name="オーラダメージ", dmg=self.kougeki.aura_damage(
            self.delivery, self.hoyuusya), from_code=UC_AURA, to_code=UC_DUST)
        can_receive_aura = _ad_card.can_damage(delivery=self.delivery, hoyuusya=self.hoyuusya)
        _ld_card = Damage(img=IMG_LIFE_DAMAGE, name="ライフダメージ", dmg=self.kougeki.life_damage(
            self.delivery, self.hoyuusya), from_code=UC_LIFE, to_code=UC_FLAIR)
        self.uke_taba = bac.maid_by_cards(cards=([_ad_card, _ld_card] if can_receive_aura else [_ld_card]), hoyuusya=self.hoyuusya)

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

    def _mousedown(self, huda: Huda) -> None:
        controller.active = huda

    def _mouseup(self, huda: Huda) -> None:
        # popup_message.add(text="PlayKougeki.mouseup でクリック確定したよ")
        huda.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya)
        if self.source_huda:
            self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
        moderator.pop()


# compatible_with(, OverLayer)
