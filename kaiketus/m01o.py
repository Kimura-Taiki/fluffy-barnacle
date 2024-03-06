#                 20                  40                  60                 79
import pygame

from mod.const import MG_YURINA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.delivery import Delivery

def kessi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_LIFE)

n_1 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_1.png"), name="斬", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

def _aura_damage_2(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if kessi(delivery, hoyuusya) else 2

n_2 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_2.png"), name="一閃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_2, life_damage_func=int_di(1), maai_list=dima_di(3, 4))

