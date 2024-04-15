from typing import runtime_checkable, Protocol

from mod.delivery import Delivery

@runtime_checkable
class _Huda(Protocol):
    delivery: Delivery
    hoyuusya: int

def amortize_default(huda: _Huda) -> None:
    huda.delivery.send_ouka_to_ryouiki(hoyuusya=huda.hoyuusya, from_huda=huda)
