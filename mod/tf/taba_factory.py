#                 20                  40                  60                 79
from pygame.surface import Surface
from typing import Callable
from functools import partial
from copy import copy

from mod.const import WX, WY, SIMOTE, KAMITE
from mod.huda import Huda
from mod.taba import Taba
from mod.card import Card

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY-150

class TabaFactory():
    def __init__(self, inject_kwargs: dict[str, Callable[[Huda], None]],
                 huda_x: Callable[[int, int], float]=HAND_X,
                 huda_y: Callable[[int, int], float]=HAND_Y,
                 huda_angle: Callable[[int, int], float]=HAND_ANGLE,
                 is_ol: bool=False) -> None:
        self.inject_kwargs = inject_kwargs
        self.main_phase_inject_kwargs = inject_kwargs
        self.view_inject_kwargs = {"draw": inject_kwargs.get("draw", Huda.default_draw), "hover": Huda.detail_draw}
        self.simote_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: huda_x(i, j), lambda i, j: huda_y(i, j), lambda i, j: huda_angle(i, j))
        self.kamite_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: WX-huda_x(i, j), lambda i, j: WY-huda_y(i, j), lambda i, j: huda_angle(i, j)+180.0)
        if is_ol:
            self.kamite_funcs = self.simote_funcs

    def maid_by_files(self, surfaces: list[Surface], hoyuusya: int) -> Taba:
        taba = self._empty_taba(hoyuusya=hoyuusya)
        for i in surfaces:
            huda = Huda(img=i)
            huda.hoyuusya = hoyuusya
            taba.append(huda)
        return taba

    def maid_by_cards(self, cards: list[Card], hoyuusya: int) -> Taba:
        taba = self._empty_taba(hoyuusya=hoyuusya)
        for card in cards:
            huda = Huda(img=card.img)
            huda.hoyuusya = hoyuusya
            huda.card = card
            taba.append(huda)
        return taba

    def maid_by_hudas(self, hudas: list[Huda], hoyuusya: int) -> Taba:
        taba = self._empty_taba(hoyuusya=hoyuusya)
        for huda in hudas:
            proxy_huda = copy(huda)
            proxy_huda.base = huda
            taba.append(proxy_huda)
        return taba

    def _empty_taba(self, hoyuusya: int) -> Taba:
        taba = Taba(hoyuusya=hoyuusya, inject=self._inject)
        taba.main_phase_inject_kwargs = self.main_phase_inject_kwargs
        taba.view_inject_kwargs = self.view_inject_kwargs
        taba.rearrange = partial(self._rearrange_huda, taba=taba, hoyuusya=hoyuusya)
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
