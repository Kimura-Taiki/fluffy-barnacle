from typing import Protocol, runtime_checkable

from mod.huda import Huda

@runtime_checkable
class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        ...