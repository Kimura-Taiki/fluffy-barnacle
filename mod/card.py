#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any
from functools import partial

from mod.const import CT_HUTEI, CT_KOUGEKI, draw_aiharasuu, UC_MAAI, TC_SUTEHUDA, SIMOTE, KAMITE, side_name, UC_FLAIR\
    , CT_KOUDOU, UC_DUST, USAGE_DEPLOYED
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.moderator import moderator

BoolDI = Callable[[Delivery, int], bool]
KoukaDI = Callable[[Delivery, int], None]
SuuziDI = Callable[[Delivery, int], int]
MaaiDI = Callable[[Delivery, int], list[bool]]
TaiounizeDI = Callable[['Card', Delivery, int], 'Card']
auto_di: BoolDI = lambda delivery, hoyuusya: True
pass_di: KoukaDI = lambda delivery, hoyuusya: None
int_di: Callable[[int], SuuziDI] = lambda i: lambda delivery, hoyuusya: i
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: lambda delivery, hoyuusya: [j == i for j in range(11)]
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: lambda delivery, hoyuusya: [i <= k <= j for k in range(11)]
identity_di: TaiounizeDI = lambda i, j, k: i

#                 20                  40                  60                 79
class Card():
    def __init__(
            self, img: Surface, name: str, cond: BoolDI, type: int=CT_HUTEI,
            aura_damage: SuuziDI = int_di(0), life_damage: SuuziDI=int_di(0),
            maai_list: MaaiDI=whole_di,
            kouka: KoukaDI=pass_di,
            osame: SuuziDI = int_di(0), suki: BoolDI=auto_di,
            tenkaizi: KoukaDI=pass_di, hakizi: KoukaDI=pass_di,
            taiou: bool=False, zenryoku: bool=False, kirihuda: bool=False,
            flair: SuuziDI=int_di(0), taiounize: TaiounizeDI = identity_di
            ) -> None:
        self.img, self.name, self.cond, self.type = img, name, cond, type
        self.aura_damage, self.life_damage, self.maai_list = aura_damage, life_damage, maai_list
        self.kouka =kouka
        self.osame, self.suki, self.tenkaizi, self.hakizi = osame, suki, tenkaizi, hakizi
        self.taiou = taiou
        self.flair = flair
        self.zenryoku = zenryoku
        self.kirihuda = kirihuda
        self.taiounize = taiounize

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        if self.kirihuda:
            delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_FLAIR, to_mine=False, to_code=UC_DUST,
                                          kazu=self.flair(delivery, hoyuusya))
        if self.type == CT_KOUDOU:
            self.kouka(delivery, hoyuusya)
            # from mod.huda import Huda
            from mod.huda import Huda
            if isinstance(huda, Huda):
                huda.discard()
            self.close(hoyuusya=hoyuusya)
        elif self.type == CT_KOUGEKI:
            from mod.ol.play_kougeki import PlayKougeki
            moderator.append(over_layer=PlayKougeki(kougeki=self, delivery=delivery, hoyuusya=hoyuusya, huda=huda))
        else:
            popup_message.add("メインタイプの解決がまだ未実装だね")
            from mod.huda import Huda
            if isinstance(huda, Huda):
                popup_message.add("付与を捨てるよ")
                huda.usage = USAGE_DEPLOYED
                huda.osame = self.osame(delivery, hoyuusya)
                huda.discard()
            self.close(hoyuusya=hoyuusya)

    def is_full(self, delivery: Delivery, hoyuusya: int) -> bool:
        return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_FLAIR) >= self.flair(delivery, hoyuusya)

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        if not self.cond(delivery, hoyuusya):
            popup_message.add(text=f"「{self.name}」の使用条件を満たしていません")
            return False
        elif not self.is_full(delivery=delivery, hoyuusya=hoyuusya):
            popup_message.add(text=f"「{self.name}」に費やすフレアが足りません")
            return False
        elif self.type == CT_KOUGEKI and not self.maai_cond(delivery=delivery, hoyuusya=hoyuusya):
            popup_message.add(text=f"「{self.name}」の適正距離から外れています")
            return False
        return True

    def close(self, hoyuusya: int) -> None:
        popup_message.add(f"{side_name(hoyuusya)}の「{self.name}」を解決しました")

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

    def maai_cond(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.maai_list(delivery, hoyuusya)[delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_MAAI)]

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
