#                 20                  40                  60                 79
from typing import Any

from mod.const import WX, WY, POP_TAIOUED
from mod.huda import Huda
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat

class PlayTaiou():
    name = "対応時にstat戻り値を与える為の空OverLayer"

    def __init__(self, huda: Huda) -> None:
        self.huda = huda
        self.delivery = huda.delivery
        self.inject_func = huda.delivery.inject_view

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.huda.card.kaiketu(delivery=self.huda.delivery, hoyuusya=self.huda.hoyuusya, huda=self.huda)
        moderator.pop()

    def close(self) -> PopStat:
        return PopStat(code=POP_TAIOUED, huda=self.huda)

    def moderate(self, stat: PopStat) -> None:
        ...

# compatible_with(, OverLayer)
