#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol
from copy import copy

from mod.const import CF_SCALAR_CORRECTION, enforce
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDIIC, auto_diic, mine_cf, duck_card

__all__ = ['BoolDIIC', 'auto_diic', 'mine_cf']

class ScalarCorrection(Continuous):
    def __init__(self, name: str, cond: BoolDIIC, scalar: int, value: int) -> None:
        self.name = name
        self.type = CF_SCALAR_CORRECTION
        self.cond = cond
        self.scalar = scalar
        self.value = value

def applied_scalar(i: int, scalar: int, delivery: Delivery, hoyuusya: int) -> int:
    cfs: list[ScalarCorrection] = delivery.cfs(type=CF_SCALAR_CORRECTION, hoyuusya=hoyuusya, card=duck_card)
    for cf in (cf for cf in cfs if cf.scalar == scalar):
        i += cf.value
    return i
