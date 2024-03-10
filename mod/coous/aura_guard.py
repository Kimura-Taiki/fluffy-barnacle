#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable, Protocol
from copy import copy

from mod.const import CF_AURA_GUARD, enforce, TC_SUTEHUDA, UC_AURA
from mod.delivery import Delivery
from mod.huda.huda import Huda
from mod.taba import Taba
from mod.coous.continuous import Continuous, BoolDIIC, auto_diic, mine_cf, duck_card

__all__ = ['BoolDIIC', 'auto_diic', 'mine_cf']

# class _Card():
#     megami = -1

class AuraGuard(Continuous):
    def __init__(self, name: str, cond: BoolDIIC) -> None:
        self.name = name
        self.type = CF_AURA_GUARD
        self.cond = cond

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"

def huyo_aura_guard(delivery: Delivery, hoyuusya: int) -> int:
    i = 0
    cfs: list[AuraGuard] = delivery.cfs(type=CF_AURA_GUARD, hoyuusya=hoyuusya, card=duck_card)
    taba = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba)
    for cf in cfs:
        huda = enforce(next((huda for huda in taba if isinstance(huda.card.cfs[0], AuraGuard)), None), Huda)
        i += huda.osame
    return i

def aura_guard_huda(delivery: Delivery, hoyuusya: int) -> Huda:
    cfs: list[AuraGuard] = delivery.cfs(type=CF_AURA_GUARD, hoyuusya=hoyuusya, card=duck_card)
    taba = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba)
    return enforce(next((huda for huda in taba if isinstance(huda.card.cfs[0], AuraGuard)), None), Huda)