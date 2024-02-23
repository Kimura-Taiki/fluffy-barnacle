#                 20                  40                  60                 79
from typing import Any, Callable

from mod.const import TC_HUSEHUDA, TC_SUTEHUDA, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, enforce, UC_SYUUTYUU, UC_ZYOGAI, POP_OK
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda import Huda
from mod.ol.undo_mouse import make_undo_youso
from mod.tf.taba_factory import TabaFactory
from mod.card import Card
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat
from mod.popup_message import popup_message
from mod.youso import Youso

def obal_func(cards: list[Card]=[], name: str="", text: str="", mode: int=OBAL_KIHONDOUSA, code: int=POP_OK) -> Callable[[Youso], None]:
    def func(youso: Youso) -> None:
        if len(cards) == 1 and not cards[0].can_play(delivery=youso.delivery, hoyuusya=youso.hoyuusya, popup=True):
            return
        if isinstance(youso, Huda) and not youso.can_standard(popup=True, is_zenryoku=mode==OBAL_USE_CARD):
            return
        if text:
            popup_message.add(text=text)
        moderator.append(over_layer=_others_basic_action_layer(
            delivery=youso.delivery, hoyuusya=youso.hoyuusya, name=name, huda=youso if
            isinstance(youso, Huda) else None,cards=cards, mode=mode, code=code))
    return func

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya, huda.base)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    mcl.delivery.m_params(mcl.hoyuusya).played_standard = True
    if mcl.mode == OBAL_KIHONDOUSA:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    elif mcl.mode == OBAL_USE_CARD:
        source_huda = enforce(mcl.source_huda, Huda)
        if source_huda.card.zenryoku:
            mcl.delivery.m_params(mcl.hoyuusya).played_zenryoku = True
        if source_huda.card.kirihuda:
            source_huda.usage = USAGE_USED
        else:
            mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    elif mcl.mode == OBAL_SYUUTYUU:
        mcl.delivery.send_ouka_to_ryouiki(
            hoyuusya=mcl.hoyuusya, from_mine=True, from_code=UC_SYUUTYUU,
            to_mine=False, to_code=UC_ZYOGAI)
    moderator.pop()

def _others_basic_action_layer(
        delivery: Delivery, hoyuusya: int, name: str="", huda: Any | None=None, cards:
        list[Card]=[], mode: int=OBAL_KIHONDOUSA, code: int=POP_OK) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(
        name=name if name else "<OthersBasicActionLayer>", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
        mode=mode, moderate=_moderate, code=code)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    if mode == OBAL_KIHONDOUSA or mode == OBAL_SYUUTYUU:
        mcl.taba = factory.maid_by_cards(cards=cards, delivery=delivery, hoyuusya=hoyuusya)
    elif mode == OBAL_USE_CARD:
        mcl.taba = factory.maid_by_hudas(hudas=[enforce(huda, Huda)], hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl
