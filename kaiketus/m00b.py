import pygame
from copy import copy
from functools import partial
from typing import Callable

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_ISYUKU, UC_AURA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO,\
    enforce, TC_TEHUDA, TC_SUTEHUDA
from mod.card import Card, auto_di, int_di, dima_di, BoolDIC, nega_dic
from mod.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import choice_layer
from mod.taba import Taba

n_1 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_1.png"), name="花弁刃", cond=auto_di, type=CT_KOUGEKI,
              aura_damage=int_di(0), aura_bar=auto_di, life_damage=int_di(1), maai_list=dima_di(4, 5))

n_2 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_2.png"), name="桜刀", cond=auto_di, type=CT_KOUGEKI,
              aura_damage=int_di(3), life_damage=int_di(1), maai_list=dima_di(3, 4))

n_3 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_3.png"), name="瞬霊式", cond=auto_di, type=CT_KOUGEKI,
              aura_damage=int_di(3), life_damage=int_di(2), maai_list=dima_di(5, 5), taiouble=nega_dic)

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_AURA, kazu=1)

def _cond_n_4(delivery: Delivery, hoyuusya: int) -> bool:
    return False
    # return delivery.b_params.during_taiou

_aan4 = TempKoudou(name="返し斬り：攻撃後", cond=_cond_n_4, kouka=_kouka_n_4, todo=[[False, UC_DUST, True, UC_AURA, 1]])

n_4 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_4.png"), name="返し斬り", cond=auto_di, type=CT_KOUGEKI,
              aura_damage=int_di(2), life_damage=int_di(1), maai_list=dima_di(3, 4), after=_aan4, taiou=True)

