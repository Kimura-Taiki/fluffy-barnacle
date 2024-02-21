#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable

from mod.const import pass_func, POP_HUYO_ELAPSED
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.moderator import moderator
from mod.ol.remove_osame.single_remove import single_remove_layer

class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya))

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        if not stat.rest_taba:
            moderator.pop()
        else:
            moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya, taba=stat.rest_taba))
