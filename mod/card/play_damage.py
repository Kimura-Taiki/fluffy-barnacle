#                 20                  40                  60                 79
from typing import Any, Protocol, runtime_checkable

from mod.const import POP_OK, UC_LIFE, opponent
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.coous.damage_2_or_more import damage_2_or_more

@runtime_checkable
class _DamageArrow(Protocol):
    from_code: int
    to_code: int
    dmg: int

class PlayDamage():
    def __init__(self, damage: _DamageArrow, delivery: Delivery, hoyuusya: int, code: int=POP_OK) -> None:
        self.da = damage
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = f"Damage：{damage.from_code}から{damage.to_code}へ{damage.dmg}点"
        self.inject_func = delivery.inject_view
        self.code = code

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.delivery.send_ouka_to_ryouiki(hoyuusya=self.hoyuusya, from_mine=False, from_code=self.da.from_code,
                                      to_mine=False, to_code=self.da.to_code, kazu=self.da.dmg)
        if self.da.dmg >= 2 and self.da.from_code == UC_LIFE:
            damage_2_or_more(delivery=self.delivery, hoyuusya=opponent(self.hoyuusya))
        if moderator.last_layer() == self:
            moderator.pop()

    def close(self) -> PopStat:
        return PopStat(self.code)

    def moderate(self, stat: PopStat) -> None:
        moderator.pop()

# compatible_with(, OverLayer)
