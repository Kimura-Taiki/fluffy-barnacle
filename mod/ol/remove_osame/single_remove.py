#                 20                  40                  60                 79
from itertools import product
from typing import Any

from mod.const import TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, UC_DUST, USAGE_USED
from mod.delivery import Delivery
from mod.huda import Huda
from mod.taba import Taba
from mod.ol.proxy_taba_factory import ProxyHuda, ProxyTabaFactory
from mod.moderator import moderator
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat

def _huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True], [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _mouseup(huda: Huda) -> None:
    if not isinstance(huda, ProxyHuda):
        raise ValueError(f"Invalid huda: {huda}")
    base = huda.base
    base.delivery.send_ouka_to_ryouiki(hoyuusya=base.hoyuusya, from_huda=base, to_mine=False, to_code=UC_DUST)
    huda.withdraw()
    if base.osame == 0:
        base.usage = USAGE_USED
        if huda.card.hakizi:
            huda.card.hakizi.kaiketu(delivery=huda.delivery, hoyuusya=huda.hoyuusya)
            return
    moderator.append(MonoChoiceLayer())
    moderator.pop()

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def single_remove_layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="償却する付与の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
                          moderate=_moderate)
    factory = ProxyTabaFactory(inject_kwargs={"mouseup": _mouseup})
    mcl.taba = factory.maid_by_cards(cards=_huyo_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)
    return mcl

