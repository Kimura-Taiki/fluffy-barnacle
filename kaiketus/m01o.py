#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import MG_YURINA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf
from mod.delivery import Delivery

def kessi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_LIFE)

n_1 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_1.png"), name="斬", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

def _aura_damage_2(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if kessi(delivery, hoyuusya) else 2

n_2 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_2.png"), name="一閃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_2, life_damage_func=int_di(1), maai_list=dima_di(3, 4))

def _taiounize_cfs_n_3(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)+1
    taiounized.aura_damage_func = aura_damage_func
    return taiounized

_cfs_n_3 = AttackCorrection(name="柄打ち", cond=mine_cf, taiounize=_taiounize_cfs_n_3)



def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).lingerings.append()

_aan3 = Card(megami=MG_YURINA, img=IMG_BYTE, name="柄打ち：攻撃後", cond=kessi, type=CT_KOUDOU, kouka=_kouka_n_3)

n_3 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_3.png"), name="柄打ち", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(1, 2), after=_aan3)
