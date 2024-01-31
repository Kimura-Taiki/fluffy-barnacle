from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import CT_HUTEI, CT_KOUGEKI
from mod.delivery import Delivery
from mod.popup_message import popup_message

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
    def __init__(self, img: Surface, name: str, cond: BoolDI) -> None:
        self.img = img
        self.name = name
        self.cond = cond
        self.type = CT_HUTEI

class Kougeki(Card):
    def __init__(self, img: Surface, name: str, cond: BoolDI,
                 aura_damage: SuuziDI, life_damage: SuuziDI, maai_list: MaaiDI) -> None:
        super().__init__(img, name, cond)
        self.type = CT_KOUGEKI
        self.aura_damage = aura_damage
        self.life_damage = life_damage
        self.maai_list = maai_list

    def attack(self, delivery: Delivery, hoyuusya: int) -> None:
        popup_message.add(text=f"{self.name}の攻撃です {self.aura_damage(delivery, hoyuusya)}/{self.life_dagage(delivery, hoyuusya)} {self.maai_text(self.maai_list(delivery, hoyuusya))}")

    def maai_text(self, bool_list: list[bool]) -> str:
        bool_list.append(False)
        text = ""
        num = -1
        chain = False
        for i, b in enumerate(bool_list):
            if b:
                if not chain:
                    num, chain = i, True
            else:
                if chain:
                    if i == num+1:
                        text, chain = text+","+str(num), False
                    else:
                        text, chain = text+","+str(num)+"-"+str(i-1), False
        return text[1:]