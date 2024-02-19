from typing import Callable

from mod.const import TC_TEHUDA, TC_KIRIHUDA, POP_TAIOUED
from mod.huda import Huda
from mod.taba import Taba
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory

def taiou_taba(delivery: Delivery, hoyuusya: int) -> Taba:
    return _taiou_factory(mouseup=_taiou_mouseup).maid_by_hudas(hudas=_taiou_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)

def _taiou_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for taba_code in [TC_TEHUDA, TC_KIRIHUDA]
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=taba_code), Taba)
        for huda in taba
        if huda.card.taiou and huda.can_play()
    ]

def _taiou_factory(mouseup: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={"mouseup": mouseup}, is_ol=True)

def _taiou_mouseup(huda: Huda) -> None:
    huda.card.kaiketu(delivery=huda.delivery, hoyuusya=huda.hoyuusya, huda=huda.base, code=POP_TAIOUED)
