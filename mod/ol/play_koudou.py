#                 20                  40                  60                 79
from typing import Any

from mod.huda import Huda
from mod.card import Card
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat

class PlayKoudou():
    def __init__(self, card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.card = card
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"行動:{card.name}の使用"
        self.inject_func = delivery.inject_view

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.card.kouka(self.delivery, self.hoyuusya)
        if moderator.last_layer() == self:
            moderator.pop()

    def close(self) -> PopStat:
        if self.source_huda:
            self.source_huda.discard()
        self.card.close(hoyuusya=self.hoyuusya)
        return PopStat()

    def moderate(self, stat: PopStat) -> None:
        moderator.pop()

# compatible_with(, OverLayer)
