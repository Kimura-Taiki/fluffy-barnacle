from typing import Callable

from mod.const import WX, WY, TC_TEHUDA, TC_KIRIHUDA
from mod.huda import Huda
from mod.taba import Taba
from mod.tf.taba_factory import TabaFactory
from mod.moderator import moderator
from mod.ol.play_taiou import PlayTaiou
from mod.delivery import Delivery

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY-150

origin_list: list[Huda] = []
taiou_taba: Taba = Taba()

def make_taiou_taba(delivery: Delivery, hoyuusya: int) -> Taba:
    global taiou_taba, origin_list
    if not isinstance(tehuda := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=TC_TEHUDA), Taba):
        raise ValueError(f"Invalid tehuda: {tehuda}")
    if not isinstance(kirihuda := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=TC_KIRIHUDA), Taba):
        raise ValueError(f"Invalid kirihuda: {kirihuda}")
    factory = _taiou_factory(mouseup=_taiou_mouseup)
    origin_list = [huda for huda in tehuda+kirihuda if huda.card.taiou]
    taiou_taba = factory.maid_by_cards(cards=[huda.card for huda in origin_list], hoyuusya=hoyuusya)
    return taiou_taba

def _taiou_factory(mouseup: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={
        "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": mouseup
        }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)

def _taiou_mouseup(huda: Huda) -> None:
    global taiou_taba, origin_list
    if (number := next((i for i, v in enumerate(taiou_taba) if v == huda))) is None:
        raise ValueError(f"Invalid huda: {huda}")
    taiou_huda = origin_list[number]
    moderator.append(over_layer=PlayTaiou(huda=taiou_huda))
