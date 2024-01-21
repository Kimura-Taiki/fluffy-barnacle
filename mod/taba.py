from typing import Callable
from functools import partial

from mod.const import nie
from mod.huda import Huda
from mod.delivery import Delivery

def _huda_taba_nie(huda: Huda, taba: 'Taba') -> None:
    nie(text="Taba.inject")

class Taba(list[Huda]):
    def __init__(self, delivery: Delivery, is_own: bool=True, rearrange: Callable[[], None]=nie(text="Taba.rearrange"),
                 inject: Callable[[Huda, 'Taba'], None]=_huda_taba_nie) -> None:
        super().__init__()
        self.delivery = delivery
        self.is_own = is_own
        self.rearrange = rearrange
        self.inject = inject
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

    @staticmethod
    def _withdraw_huda(huda: Huda, taba: 'Taba') -> None:
        taba.remove(huda)
        taba.rearrange()
