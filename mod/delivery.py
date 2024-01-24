from typing import Protocol, runtime_checkable

from mod.const import compatible_with
from mod.huda import Huda

@runtime_checkable
class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        ...

class DuckDelivery():
    def __init__(self) -> None:
        self.hoge = True
        pass

    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        pass

compatible_with(DuckDelivery(), Delivery)