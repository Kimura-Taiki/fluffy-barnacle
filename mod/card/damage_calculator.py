from typing import Protocol, Callable, Any, runtime_checkable
from copy import copy

from mod.const import CF_ATTACK_CORRECTION, enforce
from mod.delivery import Delivery

@runtime_checkable
class Attack(Protocol):
    aura_bar: Callable[[Delivery, int], bool]
    life_bar: Callable[[Delivery, int], bool]
    aura_damage_func: Callable[[Delivery, int], int]
    life_damage_func: Callable[[Delivery, int], int]

@runtime_checkable
class Coous(Protocol):
    taiounize: Callable[[Attack, Delivery, int], Attack]

def aura_damage(atk: Any, delivery: Delivery, hoyuusya: int) -> int | None:
    if not isinstance(atk, Attack) or atk.aura_bar(delivery, hoyuusya) == True:
        return None
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya)):
        return atk.aura_damage_func(delivery, hoyuusya)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.aura_damage_func(delivery, hoyuusya)

def life_damage(atk: Any, delivery: Delivery, hoyuusya: int) -> int | None:
    if not isinstance(atk, Attack) or atk.life_bar(delivery, hoyuusya) == True:
        return None
    if not (cfs := delivery.cfs(type=CF_ATTACK_CORRECTION, hoyuusya=hoyuusya)):
        return atk.life_damage_func(delivery, hoyuusya)
    kougeki = _applied_kougeki(atk=atk, cfs=cfs, delivery=delivery, hoyuusya=hoyuusya)
    return kougeki.life_damage_func(delivery, hoyuusya)

def _applied_kougeki(atk: Attack, cfs: list[Any], delivery: Delivery, hoyuusya: int) -> Attack:
    kougeki = copy(atk)
    for cf in (cf for cf in cfs if isinstance(cf, Coous)):
        kougeki = cf.taiounize(kougeki, delivery, hoyuusya)
    return kougeki