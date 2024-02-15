#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Protocol, Any, runtime_checkable
from copy import copy
from itertools import product

from mod.const import HUDA_SCALE, pass_func, WX, WY, UC_DUST, TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, USAGE_USED, screen,\
    IMG_GRAY_LAYER, POP_HUYO_ELAPSED
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.huda import Huda
from mod.tf.taba_factory import TabaFactory
from mod.taba import Taba
from mod.ol.view_banmen import view_youso
from mod.moderator import moderator

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

class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func
        self.huyo_taba = _huyo_taba(delivery=delivery, hoyuusya=hoyuusya)

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.huyo_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.huyo_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        if not self.huyo_taba:
            moderator.pop()

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        ...

def _huyo_taba(delivery: Delivery, hoyuusya: int) -> Taba:
    proxy_taba = _huyo_factory().maid_by_hudas(hudas=_huyo_hudas(delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)
    for proxy_huda in proxy_taba:
        if not isinstance(proxy_huda, _ProxyHuda):
            raise ValueError(f"Invalid huda: {proxy_huda}")
        print(proxy_huda)
    return proxy_taba

def _huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True], [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _huyo_factory() -> _NeoTabaFactory:
    return _NeoTabaFactory(inject_kwargs={
        "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": _huyo_mouseup
        }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)

def _huyo_mouseup(huda: Huda) -> None:
    raise EOFError("ここで終わり！")
    if not isinstance(huda, _ProxyHuda):
        raise ValueError(f"Invalid huda: {huda}")
    base = huda.base
    base.delivery.send_ouka_to_ryouiki(from_huda=base, to_mine=False, to_code=UC_DUST)
    base.withdraw()
