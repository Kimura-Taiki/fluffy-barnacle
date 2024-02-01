#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, BRIGHT, WX, WY, draw_aiharasuu\
    , TC_SUTEHUDA, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR
from mod.ol.over_layer import OverLayer
from mod.huda import Huda, default_draw
from mod.ol.view_banmen import view_youso
from mod.card import Card, auto_di, Kougeki, SuuziDI
from mod.taba import Taba
from mod.tf.taba_factory import TabaFactory
from mod.controller import controller
from mod.popup_message import popup_message
from mod.moderator import moderator

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
SCALE_SIZE = 180

_ad_card = Card(img=IMG_AURA_DAMAGE, name="", cond=auto_di)
_ld_card = Card(img=IMG_LIFE_DAMAGE, name="", cond=auto_di)

class PlayKougeki():
    def __init__(self, huda: Huda) -> None:
        if not isinstance(huda.card, Kougeki):
            raise ValueError(f"Invalid huda.card: {type(huda.card)}")
        self.kougeki = huda.card
        self.name = f"攻撃:{huda.card.name}の使用"
        self.source_huda = huda
        self.inject_func = huda.delivery.inject_view
        self.delivery = huda.delivery
        self.taiou_taba: Taba = Taba()
        self.uke_taba: Taba = Taba()

    def elapse(self) -> None:
        screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()
        self._draw_damage(_ad_card, self.kougeki.aura_damage)
        self._draw_damage(_ld_card, self.kougeki.life_damage)


    def get_hover(self) -> Any | None:
        return self.uke_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        bac = TabaFactory(inject_kwargs={
            "draw": self._draw, "hover": Huda.detail_draw, "mousedown": self._mousedown, "mouseup": self._mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        self.uke_taba = bac.maid_by_cards(cards=[_ad_card, _ld_card], hoyuusya=self.source_huda.hoyuusya)

    def close(self) -> int:
        return 0

    def moderate(self, stat: int) -> None:
        ...

    def _draw_damage(self, card_type: Card, damage_func: SuuziDI) -> None:
        if huda := next((huda for huda in self.uke_taba if huda.card == card_type), None):
            draw_aiharasuu(surface=screen, dest=huda.dest - Vector2(SCALE_SIZE, SCALE_SIZE)/2,
                           num=damage_func(self.delivery, self.source_huda.hoyuusya),
                           size=SCALE_SIZE)

    def _draw(self, huda: Huda) -> None:
        if controller.hover == huda:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
            screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
        else:
            default_draw(huda=huda)

    def _mousedown(self, huda: Huda) -> None:
        controller.active = huda

    def _mouseup(self, huda: Huda) -> None:
        popup_message.add(text="PlayKougeki.mouseup でクリック確定したよ")
        
        if (do := {_ad_card: self._receive_aura_damage, _ld_card: self._receive_life_damage}.get(huda.card)) is None:
            raise ValueError(f"Invalid huda.card: {huda.card}")
        do()
        huda.koudou(self.delivery, self.delivery.turn_player)
        self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
        moderator.pop()

    def _receive_aura_damage(self) -> None:
        popup_message.add(text="オーラで受けました")
        self.delivery.send_ouka_to_ryouiki(
            hoyuusya=self.source_huda.hoyuusya, from_mine=False, from_code=UC_AURA, to_mine=False, to_code=UC_DUST,
            kazu=self.kougeki.aura_damage(self.delivery, self.source_huda.hoyuusya))

    def _receive_life_damage(self) -> None:
        popup_message.add(text="ライフで受けました")
        self.delivery.send_ouka_to_ryouiki(
            hoyuusya=self.source_huda.hoyuusya, from_mine=False, from_code=UC_LIFE, to_mine=False, to_code=UC_FLAIR,
            kazu=self.kougeki.life_damage(self.delivery, self.source_huda.hoyuusya))


# compatible_with(, OverLayer)
