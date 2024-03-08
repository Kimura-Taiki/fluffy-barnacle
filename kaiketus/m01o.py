#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import MG_YURINA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.delivery import Delivery
from mod.card.kw.suki import suki_card

def kessi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_LIFE) <= 3

n_1 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_1.png"), name="斬", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

def _aura_damage_2(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if kessi(delivery, hoyuusya) else 2

n_2 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_2.png"), name="一閃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_2, life_damage_func=int_di(2), maai_list=dima_di(3, 3))

def _taiounize_cfs_n_3(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)+1
    taiounized.aura_damage_func = aura_damage_func
    return taiounized

_cond_n_3: BoolDIIC = lambda delivery, atk_h, cf_h, card: \
    mine_cf(delivery, atk_h, cf_h, card) and card.megami != MG_YURINA

_cfs_n_3 = AttackCorrection(name="柄打ち", cond=_cond_n_3, taiounize=_taiounize_cfs_n_3)

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).lingerings.append(_cfs_n_3)

_aan3 = Card(megami=MG_YURINA, img=IMG_BYTE, name="柄打ち：攻撃後", cond=kessi, type=CT_KOUDOU, kouka=_kouka_n_3)

n_3 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_3.png"), name="柄打ち", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(1, 2), after=_aan3)

def _aura_damage_4(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if delivery.ouka_count(hoyuusya=hoyuusya, is_mine=False, utuwa_code=UC_MAAI) <= 2 else 4

def _life_damage_4(delivery: Delivery, hoyuusya: int) -> int:
    return 2 if delivery.ouka_count(hoyuusya=hoyuusya, is_mine=False, utuwa_code=UC_MAAI) <= 2 else 3

n_4 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_4_s2.png"), name="居合", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_4, life_damage_func=_life_damage_4, maai_list=dima_di(2, 4), zenryoku=True)

def _taiounize_cfs_n_5(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def taiouble(delivery: Delivery, hoyuusya: int, card: Card) -> bool:
        return False if not card.kirihuda else kougeki.taiouble(delivery, hoyuusya, card)
    def maai_list(delivery: Delivery, hoyuusya: int) -> list[bool]:
        li = kougeki.maai_list(delivery, hoyuusya)
        for i, v in enumerate(li):
            if i == 0 or not v:
                continue
            li[i-1] = True
            break
        return li
    taiounized.taiouble = taiouble
    taiounized.maai_list = maai_list
    return taiounized

_cond_n_5: BoolDIIC = lambda delivery, atk_h, cf_h, card: \
    mine_cf(delivery, atk_h, cf_h, card) and card.megami != MG_YURINA and not card.kirihuda

_cfs_n_5 = AttackCorrection(name="気迫", cond=_cond_n_5, taiounize=_taiounize_cfs_n_5)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    delivery.m_params(hoyuusya).lingerings.append(_cfs_n_5)

n_5 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_5_s5.png"), name="気迫", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_5)

_hakizi_n_6 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="圧気：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_bar=auto_di, maai_list=dima_di(3, 4))

n_6 = suki_card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="圧気", cond=auto_di,
                osame=int_di(2), hakizi=_hakizi_n_6)
