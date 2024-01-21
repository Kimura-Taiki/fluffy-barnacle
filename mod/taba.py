from typing import Callable
from functools import partial

from mod.const import nie
from mod.huda import Huda

class Taba(list[Huda]):
    def __init__(self) -> None:
        super().__init__()
        self.other_params: list[int] = []
        self.rearrange: Callable[[], None] = nie(text="Taba.rearrange")

    def get_hover_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)

    def elapse(self) -> None:
        [huda.draw() for huda in self]

    def append(self, __object: Huda) -> None:
        self._has(huda=__object)
        super().append(__object)
        self.rearrange()

    def _has(self, huda: Huda) -> Huda:
        huda.withdraw = partial(self._withdraw_huda, huda=huda, taba=self)
        return huda

    @staticmethod
    def _withdraw_huda(huda: Huda, taba: 'Taba') -> None:
        taba.remove(huda)
        taba.rearrange()
