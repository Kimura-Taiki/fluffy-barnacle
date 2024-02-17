#                 20                  40                  60                 79
from typing import Callable
from functools import partial
from itertools import product

from mod.const import UC_DUST, TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, USAGE_USED
from mod.delivery import Delivery
from mod.huda import Huda
from mod.taba import Taba
from mod.ol.hakizi import Hakizi
from mod.moderator import moderator
from mod.ol.proxy_taba_factory import ProxyTabaFactory, ProxyHuda

def huyo_taba(delivery: Delivery, hoyuusya: int, pop_func: Callable[[], None]) -> Taba:
    return _huyo_factory(pop_func=pop_func).maid_by_hudas(hudas=_huyo_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)

def _huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True], [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _huyo_factory(pop_func: Callable[[], None]) -> ProxyTabaFactory:
    return ProxyTabaFactory(inject_kwargs={"mouseup": partial(_huyo_mouseup, pop_func=pop_func)})

def _huyo_mouseup(huda: Huda, pop_func: Callable[[], None]) -> None:
    if not isinstance(huda, ProxyHuda):
        raise ValueError(f"Invalid huda: {huda}")
    base = huda.base
    base.delivery.send_ouka_to_ryouiki(hoyuusya=base.hoyuusya, from_huda=base, to_mine=False, to_code=UC_DUST)
    huda.withdraw()
    if base.osame == 0:
        base.usage = USAGE_USED
        moderator.append(Hakizi(huda=base))
        return
    pop_func()
