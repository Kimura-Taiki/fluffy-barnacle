#                 20                  40                  60                 79
from typing import Any

from mod.const import TC_HUSEHUDA
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda import Huda
from mod.kihondousa import zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card
from mod.ol.undo_mouse import make_undo_youso
from mod.ol.proxy_taba_factory import ProxyTabaFactory
from mod.card import Card
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.kaiketu_layer_facotry import kaiketu_layer_factory
from mod.ol.pop_stat import PopStat

_cards: list[Card] = [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card]

def _mouseup(huda: Huda) -> None:
    moderator.append(_KihondousaKaiketu(huda=huda))

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    moderator.pop()

def others_basic_action_layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="基本動作の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
                          moderate=_moderate)
    factory = ProxyTabaFactory(inject_kwargs={"mouseup": _mouseup})
    mcl.taba = factory.maid_by_cards(cards=_cards, hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl

def _dih(delivery: Delivery, hoyuusya: int, huda: Huda) -> None:
    huda.card.kaiketu(delivery, hoyuusya)

_KihondousaKaiketu = kaiketu_layer_factory(name="の基本動作", dih=_dih)
