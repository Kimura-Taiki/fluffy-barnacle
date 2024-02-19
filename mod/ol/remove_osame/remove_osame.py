#                 20                  40                  60                 79
from typing import Callable, Any, runtime_checkable

from mod.const import pass_func, screen, IMG_GRAY_LAYER, POP_HUYO_ELAPSED, POP_HAKIZI_DID, USAGE_USED, UC_DUST, POP_EMPTY_TABA
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.taba import Taba
from mod.ol.view_banmen import view_youso
from mod.moderator import moderator
# from mod.ol.remove_osame.huyo_taba import huyo_taba
from mod.huda import Huda
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.proxy_taba_factory import ProxyHuda, ProxyTabaFactory
from mod.ol.remove_osame.single_remove import huyo_hudas, single_remove_layer

class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func
        # self.taba = single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya)
        # self.huyo_taba = Taba()
        # self.huyo_taba = huyo_taba(delivery=delivery, hoyuusya=hoyuusya, pop_func=self._pop)

    def elapse(self) -> None:
        ...
        # screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        # self.huyo_taba.elapse()

    def get_hover(self) -> Any | None:
        return None
        # return self.huyo_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya))
        # self._pop()

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        print(stat)
        if stat.code == POP_EMPTY_TABA:
            moderator.pop()
            # print("POP_EMPTY_TABA")
        else:
            # print("RestTaba:", list(stat.rest_taba))
            moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya, taba=stat.rest_taba))
    #     self._pop()

    # def _pop(self) -> None:
    #     if not self.huyo_taba:
    #         moderator.pop()

# class RemoveOsame():
#     def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
#         self.delivery = delivery
#         self.hoyuusya = hoyuusya
#         self.name = "付与の償却"
#         self.inject_func: Callable[[], None] = pass_func
#         self.huyo_taba = Taba()
#         self.huyo_taba = huyo_taba(delivery=delivery, hoyuusya=hoyuusya, pop_func=self._pop)

#     def elapse(self) -> None:
#         screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
#         self.huyo_taba.elapse()

#     def get_hover(self) -> Any | None:
#         return self.huyo_taba.get_hover_huda() or view_youso

#     def open(self) -> None:
#         self._pop()

#     def close(self) -> PopStat:
#         return PopStat(POP_HUYO_ELAPSED)

#     def moderate(self, stat: PopStat) -> None:
#         self._pop()

#     def _pop(self) -> None:
#         if not self.huyo_taba:
#             moderator.pop()
