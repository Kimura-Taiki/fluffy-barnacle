#                 20                  40                  60                 79
from typing import Any

from mod.const import TC_SUTEHUDA
from mod.huda.huda import Huda
from mod.card.card import Card
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    if mcl.source_huda:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    moderator.pop()

def choice_layer(cards: list[Card], delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="効果の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
                          moderate=_moderate)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=cards, hoyuusya=hoyuusya)
    return mcl
