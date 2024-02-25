#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Any

from mod.const import draw_aiharasuu, POP_OK, UC_LIFE
from mod.delivery import Delivery
from mod.card.card import Card, auto_di
from mod.coous.damage_2_or_more import damage_2_or_more

class Damage(Card):
    _SCALE_SIZE = 180

    def __init__(self, img: Surface, name: str, dmg: int, from_code: int, to_code: int) -> None:
        super().__init__(img, name, auto_di)
        self.img = img.copy()
        self.dmg = dmg
        self.from_code = from_code
        self.to_code = to_code
        draw_aiharasuu(surface=self.img, dest=Vector2(340, 475)/2 - Vector2(self._SCALE_SIZE, self._SCALE_SIZE)/2,
                       num=dmg, size=self._SCALE_SIZE)

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None = None, code: int = POP_OK) -> None:
        delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code,
                                      to_mine=False, to_code=self.to_code, kazu=self.dmg)
        if self.dmg >= 2 and self.from_code == UC_LIFE:
            damage_2_or_more(delivery=delivery, hoyuusya=hoyuusya)

    def can_damage(self, delivery: Delivery, hoyuusya: int) -> bool:
        return delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code, to_mine=False, to_code=self.to_code, kazu=self.dmg)

    def can_play(self, delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
        return True