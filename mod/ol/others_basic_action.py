#                 20                  40                  60                 79
from typing import Any

from mod.const import TC_HUSEHUDA
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda import Huda
from mod.ol.undo_mouse import make_undo_youso
from mod.tf.taba_factory import TabaFactory
from mod.card import Card
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    mcl.delivery.m_params(mcl.hoyuusya).played_standard = True
    mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    moderator.pop()

def others_basic_action_layer(
        delivery: Delivery, hoyuusya: int, huda: Any | None=None, cards:
        list[Card]=[]) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="基本動作の選択", delivery=delivery, hoyuusya=
                          hoyuusya, huda=huda,moderate=_moderate)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=cards, hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl
