#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable

from mod.const import pass_func, screen, IMG_GRAY_LAYER, POP_HUYO_ELAPSED
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.taba import Taba
from mod.ol.view_banmen import view_youso
from mod.moderator import moderator
from mod.ol.huyo_taba import huyo_taba

class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func
        self.huyo_taba = Taba()
        self.huyo_taba = huyo_taba(delivery=delivery, hoyuusya=hoyuusya, pop_func=self._pop)

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.huyo_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.huyo_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        self._pop()

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        ...

    def _pop(self) -> None:
        if not self.huyo_taba:
            moderator.pop()
