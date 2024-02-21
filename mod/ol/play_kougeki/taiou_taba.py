from typing import Callable

from mod.const import TC_TEHUDA, TC_KIRIHUDA, POP_TAIOUED, side_name
from mod.huda import Huda
from mod.taba import Taba
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory
from mod.card import Card
from mod.popup_message import popup_message

def taiou_taba(delivery: Delivery, hoyuusya: int, kougeki: Card, getaiouen: bool) -> Taba:
    return _taiou_factory(mouseup=_taiou_mouseup).maid_by_hudas(
        hudas=[] if getaiouen else _taiou_hudas(delivery=delivery, hoyuusya=hoyuusya, kougeki=kougeki), hoyuusya=hoyuusya)

def _taiou_hudas(delivery: Delivery, hoyuusya: int, kougeki: Card) -> list[Huda]:
    return [
        huda
        for taba_code in [TC_TEHUDA, TC_KIRIHUDA]
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=taba_code), Taba)
        for huda in taba
        if huda.card.taiou and huda.can_play() and kougeki.nontaiouble(delivery, hoyuusya, huda.card) 
        ]

def _taiou_factory(mouseup: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={"mouseup": mouseup}, is_ol=True)

def _taiou_mouseup(huda: Huda) -> None:
    popup_message.add(f"{side_name(huda.hoyuusya)}は対応して「{huda.card.name}」カードを使います")
    huda.card.kaiketu(delivery=huda.delivery, hoyuusya=huda.hoyuusya, huda=huda.base, code=POP_TAIOUED)
