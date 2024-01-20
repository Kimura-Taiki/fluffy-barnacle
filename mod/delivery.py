from typing import Protocol

from mod.huda import Huda

class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        ...