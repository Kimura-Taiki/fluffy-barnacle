#                 20                  40                  60                 79
from typing import Any

from mod.const import WX, WY, POP_TAIOUED
from mod.huda import Huda
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat
from mod.ol.over_layer import OverLayer
from mod.delivery import Delivery

def kaiketu_layer_factory(name: str, huda: Huda, stat: PopStat) -> OverLayer:
    class Kaiketu():
        def __init__(self) -> None:
            self.huda = huda
            self.delivery = huda.delivery
            self.inject_func = huda.delivery.inject_view
            self.name = name

        def elapse(self) -> None:
            ...

        def get_hover(self) -> Any | None:
            return None

        def open(self) -> None:
            self.huda.card.kaiketu(delivery=self.huda.delivery, hoyuusya=self.huda.hoyuusya, huda=self.huda)
            if moderator.last_layer() == self:
                moderator.pop()

        def close(self) -> PopStat:
            return stat

        def moderate(self, stat: PopStat) -> None:
            moderator.pop()
    return Kaiketu

# compatible_with(, OverLayer)
