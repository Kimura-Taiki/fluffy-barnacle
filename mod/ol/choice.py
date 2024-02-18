#                 20                  40                  60                 79
from typing import Any, Callable
from functools import partial

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, TC_SUTEHUDA
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card
from mod.controller import controller
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat
from mod.ol.proxy_taba_factory import ProxyTabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer

# _factory = ProxyTabaFactory(inject_kwargs={"mouseup": self._mouseup})
# taba = _factory.maid_by_cards(cards=cards, hoyuusya=self.hoyuusya)
# MonoChoiceLayer(name="効果の選択")

def _mouseup(huda: Huda, mcl: MonoChoiceLayer) -> None:
    huda.card.kaiketu(delivery=mcl.delivery, hoyuusya=mcl.hoyuusya)
    if mcl.source_huda:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    moderator.pop()

def choice_layer(cards: list[Card], delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="効果の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda)
    factory = ProxyTabaFactory(inject_kwargs={"mouseup": partial(_mouseup, mcl=mcl)})
    mcl.taba = factory.maid_by_cards(cards=cards, hoyuusya=hoyuusya)
    return mcl

# class Choice():
#     def __init__(self, cards: list[Card], delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
#         self.delivery = delivery
#         self.hoyuusya = hoyuusya
#         self.source_huda = huda if isinstance(huda, Huda) else None
#         self.name = "効果の選択"
#         self.inject_func = delivery.inject_view
#         factory = ProxyTabaFactory(inject_kwargs={"mouseup": self._mouseup})
#         self.taba = factory.maid_by_cards(cards=cards, hoyuusya=self.hoyuusya)

#     def elapse(self) -> None:
#         screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
#         self.taba.elapse()

#     def get_hover(self) -> Any | None:
#         return self.taba.get_hover_huda() or view_youso

#     def open(self) -> None:
#         ...

#     def close(self) -> PopStat:
#         return PopStat()

#     def moderate(self, stat: PopStat) -> None:
#         ...

#     def _mouseup(self, huda: Huda) -> None:
#         # popup_message.add(text="PlayKougeki.mouseup でクリック確定したよ")
#         huda.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya)
#         if self.source_huda:
#             self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
#         moderator.pop()


# # compatible_with(, OverLayer)
