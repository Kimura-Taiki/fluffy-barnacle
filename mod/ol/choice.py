#                 20                  40                  60                 79
from typing import Any
from functools import partial

from mod.const import TC_SUTEHUDA
from mod.huda import Huda
from mod.card import Card
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.proxy_taba_factory import ProxyTabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.kaiketu_layer_facotry import kaiketu_layer_factory
from mod.ol.pop_stat import PopStat

def _mouseup(huda: Huda, mcl: MonoChoiceLayer) -> None:
    moderator.append(ChoiceKaiketu(huda=huda))

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    if mcl.source_huda:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    moderator.pop()

def choice_layer(cards: list[Card], delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="効果の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
                          moderate=_moderate)
    factory = ProxyTabaFactory(inject_kwargs={"mouseup": partial(_mouseup, mcl=mcl)})
    mcl.taba = factory.maid_by_cards(cards=cards, hoyuusya=hoyuusya)
    return mcl

def _dih(delivery: Delivery, hoyuusya: int, huda: Huda) -> None:
    huda.card.kaiketu(delivery, hoyuusya)

ChoiceKaiketu = kaiketu_layer_factory(name="を選択", dih=_dih)
