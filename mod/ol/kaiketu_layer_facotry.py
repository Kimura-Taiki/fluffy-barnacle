#                 20                  40                  60                 79
from typing import Any, Callable

from mod.const import POP_OK
from mod.huda import Huda
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat
from mod.delivery import Delivery

class Kaiketu():
    inject_name: str = ""
    inject_code: int = 0
    def __init__(self, huda: Huda) -> None:
        self.huda = huda
        self.delivery = huda.delivery
        self.hoyuusya = huda.hoyuusya
        self.inject_func = huda.delivery.inject_view
        self.name = huda.card.name+self.inject_name
        self.inject_dih: Callable[[Delivery, int, Huda], None] = lambda delivery, hoyuusya, huda: None

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.inject_dih(self.delivery, self.hoyuusya, self.huda)
        if moderator.last_layer() == self:
            moderator.pop()

    def close(self) -> PopStat:
        return PopStat(code=self.inject_code, huda=self.huda)

    def moderate(self, stat: PopStat) -> None:
        moderator.pop()

def kaiketu_layer_factory(name: str, code: int=POP_OK, dih: Callable[
    [Delivery, int, Huda], None]=lambda delivery, hoyuusya, huda: None) -> type[Kaiketu]:
    class ConcreteKaiketu(Kaiketu):
        inject_name = name
        inject_code = code
        def __init__(self, huda: Huda) -> None:
            super().__init__(huda)
            self.inject_dih = dih
    return ConcreteKaiketu

# compatible_with(, OverLayer)
