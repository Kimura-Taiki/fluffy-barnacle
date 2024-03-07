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
    maai_list_func: Callable[[Delivery, int], list[bool]]
    taiouble_func: Callable[[Delivery, int, Any], bool]

TaiounizeDI = Callable[[Attack, Delivery, int], Attack]

class AttackCorrection(Continuous):
    def __init__(self, name: str, cond: BoolDIIC, taiounize: TaiounizeDI) -> None:
        self.name = name
        self.type = CF_ATTACK_CORRECTION
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"

def aura_damage(atk: Any, delivery: Delivery, hoyuusya: int) -> int | None:
    if not isinstance(atk, Attack) or atk.aura_bar(delivery, hoyuusya) == True:
        return None
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya, card=atk)):
        return atk.aura_damage_func(delivery, hoyuusya)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.aura_damage_func(delivery, hoyuusya)

def life_damage(atk: Any, delivery: Delivery, hoyuusya: int) -> int | None:
    if not isinstance(atk, Attack) or atk.life_bar(delivery, hoyuusya) == True:
        return None
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya, card=atk)):
        return atk.life_damage_func(delivery, hoyuusya)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.life_damage_func(delivery, hoyuusya)

def maai_list(atk: Any, delivery: Delivery, hoyuusya: int) -> list[bool]:
    if not isinstance(atk, Attack):
        return [False]*11
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya, card=atk)):
        return atk.maai_list_func(delivery, hoyuusya)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.maai_list_func(delivery, hoyuusya)

def taiouble(atk: Any, delivery: Delivery, hoyuusya: int, counter_card: Any) -> bool:
    if not isinstance(atk, Attack):
        return False
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya, card=atk)):
        return atk.taiouble_func(delivery, hoyuusya, counter_card)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.taiouble_func(delivery, hoyuusya, counter_card)

def _applied_kougeki(atk: Attack, cfs: list[Any], delivery: Delivery, hoyuusya: int) -> Attack:
    kougeki = copy(atk)
    for cf in (cf for cf in cfs if isinstance(cf, AttackCorrection)):
        kougeki = cf.taiounize(kougeki, delivery, hoyuusya)
    return kougeki
