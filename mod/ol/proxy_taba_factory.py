#                 20                  40                  60                 79
from typing import Callable
from functools import partial

from mod.const import WX, WY
from mod.huda import Huda
from mod.tf.taba_factory import TabaFactory
from mod.taba import Taba

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY-150

class ProxyHuda(Huda):
    def __init__(self, base: Huda) -> None:
        base_attributes = vars(base)
        for key, value in base_attributes.items():
            setattr(self, key, value)
        self.base = base

class ProxyTabaFactory(TabaFactory):
    def __init__(self, inject_kwargs: dict[str, Callable[[Huda], None]], huda_x: Callable[[int, int], float]=HAND_X,
                 huda_y: Callable[[int, int], float]=HAND_Y, huda_angle: Callable[[int, int], float]=HAND_ANGLE) -> None:
        base_inject_kwargs = {"draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown}
        super().__init__(base_inject_kwargs | inject_kwargs, huda_x, huda_y, huda_angle)
        self.kamite_funcs = self.simote_funcs

    def maid_by_hudas(self, hudas: list[Huda], hoyuusya: int) -> Taba:
        taba = Taba(hoyuusya=hoyuusya, inject=self._inject)
        taba.main_phase_inject_kwargs = self.main_phase_inject_kwargs
        taba.view_inject_kwargs = self.view_inject_kwargs
        taba.rearrange = partial(self._rearrange_huda, taba=taba, hoyuusya=hoyuusya)
        for huda in hudas:
            proxy_huda = ProxyHuda(base=huda)
            taba.append(proxy_huda)
        return taba
