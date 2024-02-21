#                 20                  40                  60                 79
from typing import Any

from mod.const import TC_HUSEHUDA, TC_SUTEHUDA, OBAL_KIHONDOUSA, OBAL_SYUUTYUU, OBAL_USE_CARD, enforce
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda import Huda
from mod.ol.undo_mouse import make_undo_youso
from mod.tf.taba_factory import TabaFactory
from mod.card import Card
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya, huda.base)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    mcl.delivery.m_params(mcl.hoyuusya).played_standard = True
    if mcl.mode == OBAL_KIHONDOUSA:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    # elif mcl.mode == OBAL_USE_CARD:
    #     mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    moderator.pop()

def others_basic_action_layer(
        delivery: Delivery, hoyuusya: int, huda: Any | None=None, cards:
        list[Card]=[], mode: int=OBAL_KIHONDOUSA) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(
        name="基本動作の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
        mode=mode, moderate=_moderate)
#                 20                  40                  60                 79
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    if mode == OBAL_KIHONDOUSA:
        mcl.taba = factory.maid_by_cards(cards=cards, hoyuusya=hoyuusya)
    elif mode == OBAL_USE_CARD:
        mcl.taba = factory.maid_by_hudas(hudas=[enforce(huda, Huda)], hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl
