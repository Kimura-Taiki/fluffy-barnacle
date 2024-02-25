#                 20                  40                  60                 79
from typing import Callable, TypeVar, Any

from mod.const import CF_ATTACK_CORRECTION
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDII, auto_dii

__all__ = ['BoolDII']

_T = TypeVar('_T')
TaiounizeDI = Callable[[_T, Delivery, int], _T]

class AttackCorrection(Continuous):
    def __init__(self, name: str, cond: BoolDII=auto_dii, taiounize: TaiounizeDI[Any] | None=None) -> None:
        self.name = name
        self.type = CF_ATTACK_CORRECTION
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"
