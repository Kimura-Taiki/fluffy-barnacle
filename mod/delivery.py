from typing import Protocol, runtime_checkable, Any, NamedTuple

from mod.const import compatible_with

@runtime_checkable
class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        ...

    def can_ouka_to_ryouiki(self, listener: Any, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        ...

    def send_ouka_to_ryouiki(self, listener: Any, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        ...

class _DuckDelivery():
    def __init__(self) -> None:
        pass

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        pass

    def can_ouka_to_ryouiki(self, listener: Any, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        pass

    def send_ouka_to_ryouiki(self, listener: Any, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        pass


duck_delivery = _DuckDelivery()

@runtime_checkable
class Listener(Protocol):
    delivery: Delivery
    hoyuusya: int

    def tenko(self) -> list['Listener']:
        ...

compatible_with(_DuckDelivery(), Delivery)
