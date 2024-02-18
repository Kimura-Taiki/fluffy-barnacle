#                 20                  40                  60                 79
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.taba import Taba

class MonoChoiceLayer():
    def __init__(self, name: str, taba: Taba, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        self.name = name
        self.taba = taba
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.inject_func = delivery.inject_view

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Any | None:
        return self.taba.get_hover_huda() or view_youso

    def open(self) -> None:
        ...

    def close(self) -> PopStat:
        return PopStat()

    def moderate(self, stat: PopStat) -> None:
        ...

# compatible_with(, OverLayer)
