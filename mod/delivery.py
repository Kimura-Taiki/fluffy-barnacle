from typing import Protocol, runtime_checkable, Any, NamedTuple

from mod.const import compatible_with

@runtime_checkable
class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        ...

class _DuckDelivery():
    def __init__(self) -> None:
        self.hoge = True
        pass

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        pass

duck_delivery = _DuckDelivery()

@runtime_checkable
class Listener(Protocol):
    delivery: Delivery
    hoyuusya: int

    def tenko(self) -> list['Listener']:
        ...

compatible_with(_DuckDelivery(), Delivery)
