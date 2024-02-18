#                 20                  40                  60                 79
import pygame
from typing import Callable, Any
from functools import partial

from mod.const import compatible_with, pass_func, screen, IMG_GRAY_LAYER, TC_HUSEHUDA
from mod.delivery import Delivery, duck_delivery
from mod.moderator import moderator
from mod.ol.over_layer import OverLayer
from mod.taba import Taba
from mod.youso import Youso
from mod.huda import Huda
from mod.controller import controller
from mod.kihondousa import zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card
from mod.ol.undo_mouse import make_undo_youso
from mod.ol.pop_stat import PopStat
from mod.ol.proxy_taba_factory import ProxyTabaFactory
from mod.card import Card
from mod.ol.mc_layer_factory import MonoChoiceLayer

_cards: list[Card] = [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card]

_undo_youso = make_undo_youso(text="OthersBasicAction")

def _mouseup(huda: Huda, mcl: MonoChoiceLayer) -> None:
    huda.card.kaiketu(delivery=mcl.delivery, hoyuusya=mcl.hoyuusya)
    mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    moderator.pop()

def others_basic_action_layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="基本動作の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda)
    factory = ProxyTabaFactory(inject_kwargs={"mouseup": partial(_mouseup, mcl=mcl)})
    mcl.taba = factory.maid_by_cards(cards=_cards, hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl

# class OthersBasicAction():
#     def __init__(self, huda: Huda, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
#         self.name = "基本動作の選択"
#         self.source_huda = huda
#         self.inject_func: Callable[[], None] = inject_func
#         self.delivery = delivery
#         self.hoyuusya = huda.hoyuusya
#         self.taba: Taba

#     def elapse(self) -> None:
#         screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
#         self.taba.elapse()

#     def get_hover(self) -> Youso | None:
#         return self.taba.get_hover_huda() or _undo_youso

#     def open(self) -> None:
#         factory = ProxyTabaFactory(inject_kwargs={"mouseup": self._mouseup})
#         self.taba = factory.maid_by_cards(cards=_cards, hoyuusya=self.delivery.turn_player)

#     def close(self) -> PopStat:
#         return PopStat()

#     def moderate(self, stat: PopStat) -> None:
#         ...

#     def _mouseup(self, huda: Huda) -> None:
#         huda.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya)
#         self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
#         moderator.pop()

# compatible_with(OthersBasicAction(Huda(img=pygame.Surface((16, 16)))), OverLayer)