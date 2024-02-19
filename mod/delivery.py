#                 20                  40                  60                 79
from typing import Protocol, runtime_checkable, Any, NamedTuple

from mod.const import compatible_with, HANTE, UC_DUST
from mod.req.request import Request
from mod.mkt.params import Params

@runtime_checkable
class Delivery(Protocol):
    turn_player: int

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        ...

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> bool:
        ...

    def send_ouka_to_ryouiki(
            self, hoyuusya: int,
            from_mine: bool=False, from_code: int=UC_DUST, from_huda: Any | None=None,
            to_mine: bool=False, to_code: int=UC_DUST, to_huda: Any | None=None,
            kazu: int=1) -> None:
        ...

    def inject_view(self) -> None:
        ...

    def taba_target(self, hoyuusya: int, is_mine: bool, taba_code: int) -> Any:
        ...

    def ouka_count(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> int:
        ...

    def respond(self, request: Request) -> Any | None:
        ...

    def hand_draw(self, hoyuusya: int, is_mine: bool) -> None:
        ...

    def params(self, hoyuusya: int) -> Params:
        ...

class _DuckDelivery():
    def __init__(self) -> None:
        self.turn_player = HANTE

    def send_huda_to_ryouiki(self, huda: Any, is_mine: bool, taba_code: int) -> None:
        pass

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int=1) -> bool:
        return False

    def send_ouka_to_ryouiki(
            self, hoyuusya: int,
            from_mine: bool=False, from_code: int=UC_DUST, from_huda: Any | None=None,
            to_mine: bool=False, to_code: int=UC_DUST, to_huda: Any | None=None,
            kazu: int=1) -> None:
        ...

    def inject_view(self) -> None:
        pass

    def taba_target(self, hoyuusya: int, is_mine: bool, taba_code: int) -> Any:
        return None

    def ouka_count(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> int:
        return 0

    def respond(self, request: Request) -> Any | None:
        return None

    def hand_draw(self, hoyuusya: int, is_mine: bool) -> None:
        ...

    def params(self, hoyuusya: int) -> Params:
        return Params()


duck_delivery = _DuckDelivery()

@runtime_checkable
class Listener(Protocol):
    delivery: Delivery
    hoyuusya: int

    def tenko(self) -> list['Listener']:
        ...

compatible_with(_DuckDelivery(), Delivery)
