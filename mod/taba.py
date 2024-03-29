from typing import Callable, SupportsIndex
from functools import partial

from mod.const import nie, compatible_with, SIMOTE, pass_func, enforce
from mod.huda.huda import Huda
from mod.delivery import Listener, Delivery, duck_delivery
from mod.mkt.core_view import CoreView

def _huda_taba_nie(huda: Huda, taba: 'Taba') -> None:
    nie(text="Taba.inject")

class Taba(list[Huda]):
    def __init__(self, hoyuusya: int=SIMOTE, rearrange: Callable[[], None]=nie(text="Taba.rearrange"),
                 inject: Callable[[Huda, 'Taba'], None]=_huda_taba_nie) -> None:
        super().__init__()
        self.delivery: Delivery = duck_delivery
        self.hoyuusya = hoyuusya
        self.rearrange = rearrange
        self.inject = inject
        self.main_phase_inject_kwargs: dict[str, Callable[[Huda], None]] = {"hoge": pass_func}
        self.view_inject_kwargs: dict[str, Callable[[Huda], None]] = {"hoge": pass_func}
        self.withdraw: Callable[[], None] = nie(text="Taba.withdraw")

    def get_hover_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)

    def elapse(self) -> None:
        [huda.draw() for huda in self]

    def append(self, __object: Huda) -> None:
        self.inject(__object, self)
        __object.withdraw = partial(self._withdraw_huda, huda=__object, taba=self)
        super().append(__object)
        self.rearrange()

    def insert(self, __index: SupportsIndex, __object: Huda) -> None:
        self.inject(__object, self)
        __object.withdraw = partial(self._withdraw_huda, huda=__object, taba=self)
        super().insert(__index, __object)
        self.rearrange()

    def text(self, name: str) -> str:
        return f"{name}{len(self)}"
    
    def tenko(self) -> list[Listener]:
        return [self]+list(self)
    
    def inject_kwargs(self, kwargs: dict[str, Callable[[Huda], None]]) -> None:
        for huda in self:
            huda.inject_funcs(**kwargs)

    def __repr__(self) -> str:
        obj_type = type(self).__name__
        obj_address = hex(id(self))
        return f"<{obj_type} object at {obj_address}>"

    @staticmethod
    def _withdraw_huda(huda: Huda, taba: 'Taba') -> None:
        taba.remove(huda)
        taba.rearrange()

compatible_with(obj=Taba(), protocol=CoreView)
compatible_with(obj=Taba(), protocol=Listener)
