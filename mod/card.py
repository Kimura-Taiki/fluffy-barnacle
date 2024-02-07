from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any
from functools import partial

from mod.const import CT_HUTEI, CT_KOUGEKI, draw_aiharasuu, UC_MAAI, TC_SUTEHUDA, SIMOTE, KAMITE, side_name
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.req.req_ouka import ReqOuka

BoolDI = Callable[[Delivery, int], bool]
KoukaDI = Callable[[Delivery, int], None]
SuuziDI = Callable[[Delivery, int], int]
MaaiDI = Callable[[Delivery, int], list[bool]]
TaiounizeDI = Callable[['Kougeki', Delivery, int], 'Kougeki']
auto_di: BoolDI = lambda delivery, hoyuusya: True
pass_di: KoukaDI = lambda delivery, hoyuusya: None
int_di: Callable[[int], SuuziDI] = lambda i: lambda delivery, hoyuusya: i
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: lambda delivery, hoyuusya: [j == i for j in range(11)]
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: lambda delivery, hoyuusya: [i <= k <= j for k in range(11)]
# identity_di: Callable[['Card', Delivery, int], 'Card'] = lambda i, j, k: i
identity_di: TaiounizeDI = lambda i, j, k: i

class Card():
    def __init__(self, img: Surface, name: str, cond: BoolDI, taiou: bool=False, zenryoku: bool=False,
                 taiounize: TaiounizeDI = identity_di) -> None:
        self.img = img
        self.name = name
        self.cond = cond
        self.type = CT_HUTEI
        self.taiou = taiou
        self.zenryoku = zenryoku
        self.taiounize = taiounize

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        pass

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.cond(delivery, hoyuusya)
    
    def close(self, hoyuusya: int) -> None:
        popup_message.add(f"{side_name(hoyuusya)}の「{self.name}」を解決しました")
# TaiounizeDI = Callable[[Card, Delivery, int], Card]

class Kougeki(Card):
    # def __init__(self, img: Surface, name: str, cond: BoolDI, aura_damage: SuuziDI, life_damage: SuuziDI,
    #              maai_list: MaaiDI, taiou: bool=False, zenryoku: bool=False) -> None:
    def __init__(self, img: Surface, name: str, cond: BoolDI, aura_damage: SuuziDI, life_damage: SuuziDI,
                 maai_list: MaaiDI, taiou: bool = False, zenryoku: bool = False, taiounize: TaiounizeDI = identity_di) -> None:
        super().__init__(img, name, cond, taiou, zenryoku, taiounize)
        self.type = CT_KOUGEKI
        self.aura_damage = aura_damage
        self.life_damage = life_damage
        self.maai_list = maai_list

    def attack(self, delivery: Delivery, hoyuusya: int) -> None:
        popup_message.add(text=f"{self.name}の攻撃です {self.aura_damage(delivery, hoyuusya)}/{self.life_damage(delivery, hoyuusya)} {self.maai_text(self.maai_list(delivery, hoyuusya))}")

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

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        from mod.ol.play_kougeki import PlayKougeki
        moderator.append(over_layer=PlayKougeki(kougeki=self, delivery=delivery, hoyuusya=hoyuusya, huda=huda))

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.cond(delivery, hoyuusya) and self.maai_cond(delivery=delivery, hoyuusya=hoyuusya)

    def maai_cond(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.maai_list(delivery, hoyuusya)[delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_MAAI)]

class Koudou(Card):
    def __init__(self, img: Surface, name: str, cond: BoolDI, kouka: KoukaDI, taiou: bool=False, zenryoku: bool=False,
                 taiounize: TaiounizeDI = identity_di) -> None:
        super().__init__(img, name, cond, taiou, zenryoku, taiounize)
        self.kouka = kouka

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None = None) -> None:
        self.kouka(delivery, hoyuusya)
        if huda:
            delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_SUTEHUDA)
        self.close(hoyuusya=hoyuusya)

class Damage(Card):
    _SCALE_SIZE = 180

    def __init__(self, img: Surface, name: str, dmg: int, from_code: int, to_code: int) -> None:
        super().__init__(img, name, auto_di)
        self.img = img.copy()
        self.dmg = dmg
        self.from_code = from_code
        self.to_code = to_code
        draw_aiharasuu(surface=self.img, dest=Vector2(340, 475)/2 - Vector2(self._SCALE_SIZE, self._SCALE_SIZE)/2,
                       num=dmg, size=self._SCALE_SIZE)

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code,
                                      to_mine=False, to_code=self.to_code, kazu=self.dmg)

    def can_damage(self, delivery: Delivery, hoyuusya: int) -> bool:
        return delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code, to_mine=False, to_code=self.to_code, kazu=self.dmg)

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        return True
