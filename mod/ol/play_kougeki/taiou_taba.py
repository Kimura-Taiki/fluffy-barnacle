from typing import Callable

from mod.const import WX, WY, TC_TEHUDA, TC_KIRIHUDA, opponent
from mod.huda import Huda
from mod.taba import Taba
from mod.moderator import moderator
from mod.ol.play_taiou import PlayTaiou
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.ol.proxy_taba_factory import ProxyTabaFactory, ProxyHuda

def _taiou_factory(mouseup: Callable[[Huda], None]) -> ProxyTabaFactory:
    return ProxyTabaFactory(inject_kwargs={
        "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": mouseup})

def _taiou_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for taba_code in [TC_TEHUDA, TC_KIRIHUDA]
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=taba_code), Taba)
        for huda in taba
        if huda.card.taiou and huda.can_play()
    ]

def taiou_taba(delivery: Delivery, hoyuusya: int) -> Taba:
    proxy_taba = _taiou_factory(mouseup=_taiou_mouseup).maid_by_hudas(hudas=_taiou_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)
    for proxy_huda in proxy_taba:
        if not isinstance(proxy_huda, ProxyHuda):
            raise ValueError(f"Invalid huda: {proxy_huda}")
        proxy_huda.redraw()
    return proxy_taba

def _taiou_mouseup(huda: Huda) -> None:
    if not isinstance(huda, ProxyHuda):
        raise ValueError(f"Invalid huda: {huda}")
    moderator.append(over_layer=PlayTaiou(huda=huda.base))