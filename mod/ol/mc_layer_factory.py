#                 20                  40                  60                 79
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, HANTE
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.taba import Taba

class MonoChoiceLayer():
    def __init__(self, name: str="", taba: Taba=Taba(), delivery: Delivery=
                 duck_delivery, hoyuusya: int=HANTE, huda: Any | None=None
                 ) -> None:
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

# def mc_layer_factory(name: str, code: int, dih: Callable[[Delivery, int, Huda], None]) -> type[MonoChoiceLayer]:
#     class ConcreteMnonoChoiceLayer(MonoChoiceLayer):
#         inject_name = name
#         inject_code = code
#         def __init__(self, huda: Huda) -> None:
#             super().__init__(huda)
#             self.inject_dih = dih
#     return ConcreteMnonoChoiceLayer



# compatible_with(, OverLayer)
        

