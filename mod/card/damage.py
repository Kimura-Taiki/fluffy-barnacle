#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Any

from mod.const import draw_aiharasuu, POP_OK, DMG_DEFAULT, FONT_SIZE_DAMAGE
from mod.delivery import Delivery
from mod.card.card import Card, auto_di
from mod.moderator import moderator
from mod.card.damage_layer import damage_layer

class Damage(Card):
    def __init__(self, img: Surface, name: str, dmg: int, from_code: int,
    to_code: int, attr: int=DMG_DEFAULT) -> None:
        super().__init__(img, name, auto_di)
        self.img = img.copy()
        self.dmg = dmg
        self.from_code = from_code
        self.to_code = to_code
        self.attr = attr
        draw_aiharasuu(surface=self.img, dest=Vector2(340, 475)/2-Vector2(
            FONT_SIZE_DAMAGE, FONT_SIZE_DAMAGE)/2, num=dmg,
            size=FONT_SIZE_DAMAGE)

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None = None, code: int = POP_OK) -> None:
        moderator.append(damage_layer(card=self, delivery=delivery, hoyuusya=hoyuusya, code=code))

    def can_damage(self, delivery: Delivery, hoyuusya: int) -> bool:
        return delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code, to_mine=False, to_code=self.to_code, kazu=self.dmg)

    def can_play(self, delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
        return True