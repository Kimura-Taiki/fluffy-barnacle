#                 20                  40                  60                 79
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, SIMOTE, KAMITE
from mod.huda import Huda
from mod.taba import Taba
from mod.delivery import Delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class TabaFactory():
    def __init__(self, delivery: Delivery, inject_kwargs: dict[str, Callable[[Huda], None]],
                 huda_x: Callable[[int, int], float], huda_y: Callable[[int, int], float],
                 huda_angle: Callable[[int, int], float]) -> None:
        self.delivery, self.inject_kwargs = delivery, inject_kwargs
        self.simote_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: huda_x(i, j), lambda i, j: huda_y(i, j), lambda i, j: huda_angle(i, j))
        self.kamite_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: WX-huda_x(i, j), lambda i, j: WY-huda_y(i, j), lambda i, j: huda_angle(i, j)+180.0)
        
    def maid_by_files(self, surfaces: list[Surface], delivery: Delivery, hoyuusya: int) -> Taba:
        taba = Taba(delivery=delivery, hoyuusya=hoyuusya, inject=self._inject)
        taba.rearrange = partial(self._rearrange_huda, taba=taba, hoyuusya=hoyuusya)
        for i in surfaces:
            taba.append(Huda(img=i))
        return taba

    def _rearrange_huda(self, taba: Taba, hoyuusya: int) -> None:
        if not (funcs := {SIMOTE: self.simote_funcs, KAMITE: self.kamite_funcs}.get(hoyuusya)):
            raise ValueError(f"Invalid hoyuusya: {hoyuusya}")
        l = len(taba)
        x_func, y_func, a_func = partial(funcs[0], j=l), partial(funcs[1], j=l), partial(funcs[2], j=l)
        for i, huda in enumerate(taba):
            huda.rearrange(angle=a_func(i), scale=0.6, x=x_func(i), y=y_func(i))

    def _inject(self, huda: Huda, taba: Taba) -> None:
        huda.inject_funcs(**self.inject_kwargs)
