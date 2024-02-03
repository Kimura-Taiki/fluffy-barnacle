from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any
from functools import partial

from mod.const import CT_HUTEI, CT_KOUGEKI, draw_aiharasuu, UC_MAAI, TC_SUTEHUDA
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.req.req_ouka import ReqOuka

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

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        pass

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.cond(delivery, hoyuusya)

class Kougeki(Card):
    def __init__(self, img: Surface, name: str, cond: BoolDI,
                 aura_damage: SuuziDI, life_damage: SuuziDI, maai_list: MaaiDI) -> None:
        super().__init__(img, name, cond)
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
        return self.cond(delivery, hoyuusya) and self.maai_list(delivery, hoyuusya)[int(delivery.respond(request=ReqOuka(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_MAAI)))]

class Koudou(Card):
    def __init__(self, img: Surface, name: str, cond: BoolDI, kouka: KoukaDI) -> None:
        super().__init__(img, name, cond)
        self.kouka = kouka

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None = None) -> None:
        self.kouka(delivery, hoyuusya)
        if huda:
            delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_SUTEHUDA)

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

    def can_damage(self, delivery: Delivery, hoyuusya: int) -> None:
        return delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=False, from_code=self.from_code, to_mine=False, to_code=self.to_code, kazu=self.dmg)

    def can_play(self, delivery: Delivery, hoyuusya: int) -> bool:
        return True

from mod.const import IMG_HAKUSI, MS_MINCHO_COL, BLACK, IMG_FT_ARROW, IMG_FT_OUKA, FONT_SIZE_CARD_TITLE\
    , IMG_FT_MAAI, IMG_FT_DUST, IMG_FT_ZYOGAI, IMG_FT_AI_AURA, IMG_FT_AI_FLAIR, IMG_FT_AI_LIFE, IMG_FT_AI_SYUUTYUU\
    , IMG_FT_ZI_AURA, IMG_FT_ZI_FLAIR, IMG_FT_ZI_LIFE, IMG_FT_ZI_SYUUTYUU, UC_MAAI, UC_DUST, UC_ZYOGAI\
    , UC_AURA, UC_FLAIR, UC_LIFE, UC_SYUUTYUU
class TempCard(Card):
    def __init__(self, name: str, cond: BoolDI) -> None:
        self.img = IMG_HAKUSI.copy()
        self._draw_name(name=name)
        self._draw_yazirusi(from_mine=False, from_code=UC_SYUUTYUU, to_mine=False, to_code=UC_AURA, kazu=5)
        super().__init__(self.img, name, cond)

    def _draw_name(self, name: str) -> None:
        for i, mozi in enumerate(name):
            self.img.blit(source=MS_MINCHO_COL(mozi, FONT_SIZE_CARD_TITLE, BLACK), dest=[0, i*FONT_SIZE_CARD_TITLE])

    def _draw_yazirusi(self, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int) -> None:
        self.img.blit(source=self._img_target(is_mine=from_mine, utuwa_code=from_code), dest=[50, 50])
        self.img.blit(source=self._img_target(is_mine=to_mine, utuwa_code=to_code), dest=[190, 50])
        self.img.blit(source=IMG_FT_ARROW, dest=[120, 50])
        for i in range(kazu):
            self.img.blit(source=IMG_FT_OUKA, dest=[130-kazu*5+i*10, 50])

    def _img_target(self, is_mine: bool, utuwa_code: int) -> Surface:
        if not (target := (
            {UC_MAAI: IMG_FT_MAAI, UC_DUST: IMG_FT_DUST, UC_ZYOGAI: IMG_FT_ZYOGAI} |
            ({UC_AURA: IMG_FT_ZI_AURA, UC_FLAIR: IMG_FT_ZI_FLAIR, UC_LIFE: IMG_FT_ZI_LIFE, UC_SYUUTYUU: IMG_FT_ZI_SYUUTYUU}
             if is_mine else
             {UC_AURA: IMG_FT_AI_AURA, UC_FLAIR: IMG_FT_AI_FLAIR, UC_LIFE: IMG_FT_AI_LIFE,UC_SYUUTYUU: IMG_FT_AI_SYUUTYUU}))
             .get(utuwa_code)):
            raise ValueError(f"Invalid utuwa_code: {utuwa_code}")
        return target

