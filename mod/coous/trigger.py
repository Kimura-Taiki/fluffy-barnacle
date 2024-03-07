#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol
from copy import copy

from mod.const import CF_TRIGGER, enforce
from mod.delivery import Delivery
from mod.coous.continuous import Continuous, BoolDIIC, auto_diic, mine_cf, duck_card

__all__ = ['BoolDIIC', 'auto_diic', 'mine_cf']

# class _Card():
#     megami = -1

@runtime_checkable
class TriggerEffect(Protocol):
    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int) -> None:
        ...

class Trigger(Continuous):
    def __init__(self, name: str, cond: BoolDIIC, trigger: int, effect: TriggerEffect) -> None:
        self.name = name
        self.type = CF_TRIGGER
        self.cond = cond
        self.trigger = trigger
        self.effect = effect

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"

def solve_trigger_effect(delivery: Delivery, hoyuusya: int, trigger: int, code: int=0) -> None:
    effects = [enforce(cf, Trigger).effect for cf in delivery.cfs(
        type=CF_TRIGGER, hoyuusya=hoyuusya, card=duck_card) if enforce(cf, Trigger).trigger
        == trigger]
    if len(effects) == 0:
        ...
    elif len(effects) == 1:
        effects[0].kaiketu(delivery=delivery, hoyuusya=hoyuusya, huda=None, code=code)
    else:
        raise EOFError("誘発する効果が２つ以上になったね")
