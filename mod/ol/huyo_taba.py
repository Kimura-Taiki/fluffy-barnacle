from typing import Callable
from functools import partial
from itertools import product

from mod.const import WX, WY, UC_DUST, TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, USAGE_USED
from mod.delivery import Delivery
from mod.huda import Huda
from mod.tf.taba_factory import TabaFactory
from mod.taba import Taba

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY-150

class _ProxyHuda(Huda):
    def __init__(self, base: Huda) -> None:
        base_attributes = vars(base)
        for key, value in base_attributes.items():
            setattr(self, key, value)
        self.base = base

class _NeoTabaFactory(TabaFactory):
    def __init__(self, inject_kwargs: dict[str, Callable[[Huda], None]], huda_x: Callable[[int, int], float], huda_y: Callable[[int, int], float], huda_angle: Callable[[int, int], float]) -> None:
        super().__init__(inject_kwargs, huda_x, huda_y, huda_angle)
        self.kamite_funcs = self.simote_funcs

    def maid_by_hudas(self, hudas: list[Huda], hoyuusya: int) -> Taba:
        from functools import partial
        taba = Taba(hoyuusya=hoyuusya, inject=self._inject)
        taba.main_phase_inject_kwargs = self.main_phase_inject_kwargs
        taba.view_inject_kwargs = self.view_inject_kwargs
        taba.rearrange = partial(self._rearrange_huda, taba=taba, hoyuusya=hoyuusya)
        for huda in hudas:
            proxy_huda = _ProxyHuda(base=huda)
            taba.append(proxy_huda)
        return taba

def huyo_taba(delivery: Delivery, hoyuusya: int, pop_func: Callable[[], None]) -> Taba:
    proxy_taba = _huyo_factory(pop_func=pop_func).maid_by_hudas(hudas=_huyo_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)
    for proxy_huda in proxy_taba:
        if not isinstance(proxy_huda, _ProxyHuda):
            raise ValueError(f"Invalid huda: {proxy_huda}")
        proxy_huda.pre_osame = -1
    return proxy_taba

def _huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True], [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _huyo_factory(pop_func: Callable[[], None]) -> _NeoTabaFactory:
    return _NeoTabaFactory(inject_kwargs={
        "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown,
        "mouseup": partial(_huyo_mouseup, pop_func=pop_func)
        }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)

def _huyo_mouseup(huda: Huda, pop_func: Callable[[], None]) -> None:
    if not isinstance(huda, _ProxyHuda):
        raise ValueError(f"Invalid huda: {huda}")
    base = huda.base
    base.delivery.send_ouka_to_ryouiki(hoyuusya=base.hoyuusya, from_huda=base, to_mine=False, to_code=UC_DUST)
    if base.osame == 0:
        base.usage = USAGE_USED
    huda.withdraw()
    pop_func()
