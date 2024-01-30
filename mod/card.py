from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.delivery import Delivery

BoolDI = Callable[[Delivery, int], bool]
KoukaDI = Callable[[Delivery, int], None]
SuuziDI = Callable[[Delivery, int], int]
MaaiDI = Callable[[Delivery, int], list[bool]]
auto_di: BoolDI = lambda delivery, hoyuusya: True
pass_di: KoukaDI = lambda delivery, hoyuusya: None
int_di: Callable[[int], SuuziDI] = lambda i: lambda delivery, hoyuusya: i
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: lambda delivery, hoyuusya: [j == i for j in range(11)]
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: lambda delivery, hoyuusya: [i <= k <= j for k in range(11)]

class Card():
    def __init__(self, img: Surface, cond: BoolDI) -> None:
        self.img = img
        self.cond = cond

class Kougeki(Card):
    def __init__(self, img: Surface, cond: BoolDI, life_dagage: SuuziDI, aura_damage: SuuziDI, maai_list: MaaiDI) -> None:
        super().__init__(img, cond)
        self.life_dagage = life_dagage
        self.aura_damage =aura_damage
        self.maai_list = maai_list