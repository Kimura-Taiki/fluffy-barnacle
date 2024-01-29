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
int_di: Callable[[int], SuuziDI] = lambda i: partial(lambda delivery, hoyuusya, teisuu: teisuu, teisuu=i)
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: partial(lambda delivery, hoyuusya, teisuu: [j == teisuu for j in range(11)], teisuu=i)
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: partial(lambda delivery, hoyuusya, minsuu, maxsuu: [minsuu <= k and k <= maxsuu for k in range(11)], minsuu=i, maxsuu=j)

class Card():
    def __init__(self, img: Surface, cond: BoolDI) -> None:
        self.img = img
        self.cond = cond

class Kougeki(Card):
    def __init__(self, img: Surface, cond: BoolDI, aura_damage: SuuziDI, life_dagage: SuuziDI) -> None:
        super().__init__(img, cond)
