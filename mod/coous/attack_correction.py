#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol
from copy import copy

from mod.const import CF_ATTACK_CORRECTION
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDIIC, auto_diic, mine_cf

__all__ = ['BoolDIIC', 'auto_diic', 'mine_cf']

@runtime_checkable
class Attack(Protocol):
    megami: int
    kirihuda: bool
    aura_bar: Callable[[Delivery, int], bool]
    life_bar: Callable[[Delivery, int], bool]
    aura_damage_func: Callable[[Delivery, int], int]
    life_damage_func: Callable[[Delivery, int], int]
    aura_damage: Callable[[Delivery, int], int | None]
    life_damage: Callable[[Delivery, int], int | None]
    maai_list: Callable[[Delivery, int], list[bool]]
    taiouble: Callable[[Delivery, int, Any], bool]

TaiounizeDI = Callable[[Attack, Delivery, int], Attack]

class AttackCorrection(Continuous):
    def __init__(self, name: str, cond: BoolDIIC, taiounize: TaiounizeDI) -> None:
        self.name = name
        self.type = CF_ATTACK_CORRECTION
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"

def applied_kougeki(atk: Any, delivery: Delivery, hoyuusya: int) -> Attack:
    if not isinstance(atk, Attack):
        raise ValueError("Attack型以外が来るわけ無いんだわ")
    cfs = delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya, card=atk)
    kougeki = copy(atk)
    for cf in (cf for cf in cfs if isinstance(cf, AttackCorrection)):
        kougeki = cf.taiounize(kougeki, delivery, hoyuusya)
    return kougeki
