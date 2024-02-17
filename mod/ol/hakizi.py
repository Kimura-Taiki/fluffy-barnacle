#                 20                  40                  60                 79
from typing import Callable, Any

from mod.const import pass_func, POP_HAKIZI_DID
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.huda import Huda
from mod.moderator import moderator
from mod.popup_message import popup_message
from mod.ol.kaiketu_layer_facotry import kaiketu_layer_factory

def _dih(delivery: Delivery, hoyuusya: int, huda: Huda) -> None:
    huda.card.hakizi(delivery, hoyuusya)

Hakizi = kaiketu_layer_factory(name="の破棄時効果", code=POP_HAKIZI_DID, dih=_dih)

# class Hakizi():
#     def __init__(self, huda: Huda) -> None:
#         self.huda = huda
#         self.delivery = huda.delivery
#         self.hoyuusya = huda.hoyuusya
#         self.inject_func = huda.delivery.inject_view
#         self.name = f"{huda.card.name}の破棄時効果"

#     def elapse(self) -> None:
#         ...

#     def get_hover(self) -> Any | None:
#         return None

#     def open(self) -> None:
#         self.huda.card.hakizi(self.delivery, self.hoyuusya)
#         if moderator.last_layer() == self:
#             moderator.pop()

#     def close(self) -> PopStat:
#         return PopStat(POP_HAKIZI_DID)

#     def moderate(self, stat: PopStat) -> None:
#         moderator.pop()
