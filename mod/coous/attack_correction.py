#                 20                  40                  60                 79
from typing import Callable, TypeVar, Any, runtime_checkable, Protocol

from mod.const import CF_ATTACK_CORRECTION
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDII, auto_dii

__all__ = ['BoolDII']

@runtime_checkable
class Attack(Protocol):
    aura_bar: Callable[[Delivery, int], bool]
    life_bar: Callable[[Delivery, int], bool]
    aura_damage_func: Callable[[Delivery, int], int]
    life_damage_func: Callable[[Delivery, int], int]

TaiounizeDI = Callable[[Attack, Delivery, int], Attack]

class AttackCorrection(Continuous):
    def __init__(self, name: str, cond: BoolDII, taiounize: TaiounizeDI) -> None:
        self.name = name
        self.type = CF_ATTACK_CORRECTION
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"
