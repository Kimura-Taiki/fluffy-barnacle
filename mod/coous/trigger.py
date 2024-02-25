#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol
from copy import copy

from mod.const import CF_TRIGGER
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDII, auto_dii, mine_cf

__all__ = ['BoolDII', 'auto_dii', 'mine_cf']

@runtime_checkable
class TriggerEffect(Protocol):
    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int) -> None:
        ...

class Trigger(Continuous):
    def __init__(self, name: str, cond: BoolDII, trigger: int, effect: TriggerEffect) -> None:
        self.name = name
        self.type = CF_TRIGGER
        self.cond = cond
        self.trigger = trigger
        self.effect = effect

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"

