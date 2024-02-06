#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, BRIGHT, WX, WY, draw_aiharasuu\
    , TC_SUTEHUDA, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, opponent, POP_TAIOUED, side_name
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
from mod.ol.play_taiou import PlayTaiou

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_UX: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_UY: Callable[[int, int], float] = lambda i, j: WY-150
SCALE_SIZE = 180

class PlayKougeki():
    def __init__(self, kougeki: Kougeki, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.kougeki = kougeki
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"攻撃:{kougeki.name}の使用"
        self.inject_func = delivery.inject_view
        self.taiou_taba: Taba = Taba()
        self.origin_list: list[Huda] = []
        self.uke_taba: Taba = Taba()
        self.uke_factory = TabaFactory(inject_kwargs={
            "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": self._uke_mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        self.taiou_factory = TabaFactory(inject_kwargs={
            "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": self._taiou_mouseup
            }, huda_x=HAND_UX, huda_y=HAND_UY, huda_angle=HAND_ANGLE)
        self.taiou_huda: Huda | None = None

    def elapse(self) -> None:
        screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()
        self.taiou_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.uke_taba.get_hover_huda() or self.taiou_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        self._make_uke_taba()
        self._make_taiou_taba()

    def close(self) -> int:
        self.kougeki.close(hoyuusya=self.hoyuusya)
        return 0

    def moderate(self, stat: int) -> None:
        if stat != POP_TAIOUED or not self.taiou_huda:
            return
        self.taiou_taba.clear()
        if not self.kougeki.maai_cond(delivery=self.delivery, hoyuusya=self.hoyuusya):
            popup_message.add(text=f"{side_name(self.hoyuusya)}の「{self.kougeki.name}」が適正距離から外れました")
            self._discard_source()
            return
        print(self.taiou_huda.card.name)

    def _uke_mouseup(self, huda: Huda) -> None:
        huda.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya)
        popup_message.add(f"{side_name(self.hoyuusya)}の「{self.kougeki.name}」を{huda.card.name}")
        self._discard_source()

    def _discard_source(self) -> None:
        if self.source_huda:
            self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
        moderator.pop()

    def _taiou_mouseup(self, huda: Huda) -> None:
        if (number := next((i for i, v in enumerate(self.taiou_taba) if v == huda))) is None:
            raise ValueError(f"Invalid huda: {huda}")
        self.taiou_huda = self.origin_list[number]
        moderator.append(over_layer=PlayTaiou(huda=self.taiou_huda))

    def _make_uke_taba(self) -> None:
        _ad_card = Damage(img=IMG_AURA_DAMAGE, name="オーラで受けました", dmg=self.kougeki.aura_damage(
            self.delivery, self.hoyuusya), from_code=UC_AURA, to_code=UC_DUST)
        can_receive_aura = _ad_card.can_damage(delivery=self.delivery, hoyuusya=self.hoyuusya)
        _ld_card = Damage(img=IMG_LIFE_DAMAGE, name="ライフに通しました", dmg=self.kougeki.life_damage(
            self.delivery, self.hoyuusya), from_code=UC_LIFE, to_code=UC_FLAIR)
        self.uke_taba = self.uke_factory.maid_by_cards(cards=([_ad_card, _ld_card] if can_receive_aura else [_ld_card]), hoyuusya=self.hoyuusya)

    def _make_taiou_taba(self) -> None:
        from mod.const import TC_TEHUDA
        if not isinstance(tehuda := self.delivery.taba_target(hoyuusya=self.hoyuusya, is_mine=False, taba_code=TC_TEHUDA), Taba):
            raise ValueError(f"Invalid tehuda: {tehuda}")
        self.origin_list = [huda for huda in tehuda if huda.card.taiou]
        self.taiou_taba = self.taiou_factory.maid_by_cards(cards=[huda.card for huda in self.origin_list], hoyuusya=self.hoyuusya)


# compatible_with(, OverLayer)
