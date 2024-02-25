#                 20                  40                  60                 79
from typing import Protocol, runtime_checkable, Callable

from mod.const import CF_ATTACK_CORRECTION
from mod.delivery import Delivery
from mod.coous.continuous import BoolDII, auto_dii

TaiounizeDI = Callable[['_Karte', Delivery, int], '_Karte']

@runtime_checkable
class _Karte(Protocol):
    taiounize: TaiounizeDI

class AttackCorrection():
    def __init__(self, name: str, cond: BoolDII=auto_dii, taiounize: TaiounizeDI | None=None) -> None:
        self.name = name
        self.type = CF_ATTACK_CORRECTION
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"
