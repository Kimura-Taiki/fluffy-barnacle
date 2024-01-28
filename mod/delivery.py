from typing import Protocol, runtime_checkable, Any, NamedTuple

from mod.const import compatible_with, HANTE

@runtime_checkable
class Delivery(Protocol):
    turn_player: int

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        ...

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> bool:
        ...

    def send_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        ...

    def inject_view(self) -> None:
        ...


class _DuckDelivery():
    def __init__(self) -> None:
        self.turn_player = HANTE

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        pass

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> bool:
        return False

    def send_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> None:
        pass

    def inject_view(self) -> None:
        pass


duck_delivery = _DuckDelivery()

@runtime_checkable
class Listener(Protocol):
    delivery: Delivery
    hoyuusya: int

    def tenko(self) -> list['Listener']:
        ...

compatible_with(_DuckDelivery(), Delivery)
