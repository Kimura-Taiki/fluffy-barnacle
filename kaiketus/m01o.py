#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import MG_YURINA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.delivery import Delivery
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.coous.saiki import saiki_trigger
from mod.card.kw.syuutyuu import syuutyuu
from mod.card.kw.yazirusi import Yazirusi

def kessi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_LIFE) <= 3

n_1 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_1.png"), name="斬", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

def _aura_damage_2(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if kessi(delivery, hoyuusya) else 2

n_2 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_2.png"), name="一閃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_2, life_damage_func=int_di(2), maai_list=dima_di(3, 3))

_cfs_n_3 = AttackCorrection(name="柄打ち", cond=mine_cf, taiounize=lambda c, d, h: papl_attack(c, d, h, 1, 0))

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
    syuutyuu(delivery=delivery, hoyuusya=hoyuusya)
    delivery.m_params(hoyuusya).lingerings.append(_cfs_n_5)

n_5 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_5_s5.png"), name="気迫", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_5)

_hakizi_n_6 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="圧気：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_bar=auto_di, maai_list=dima_di(3, 4))

n_6 = suki_card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="圧気", cond=auto_di,
                osame=int_di(2), hakizi=_hakizi_n_6)

_cond_n_7: BoolDIIC = lambda delivery, atk_h, cf_h, card: \
    mine_cf(delivery, atk_h, cf_h, card) and card.megami != MG_YURINA

_cfs_n_7 = AttackCorrection(name="気炎万丈", cond=mine_cf, taiounize=lambda c, d, h: papl_attack(c, d, h, 1, 1))

n_7 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_7.png"), name="気炎万丈", cond=auto_di, type=CT_HUYO,
           osame=int_di(4), cfs=[_cfs_n_7], zenryoku=True)

s_1 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_s_1.png"), name="月影落", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(4), life_damage_func=int_di(4), maai_list=dima_di(3, 4), kirihuda=True, flair=int_di(7))

s_2 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_s_2_s5.png"), name="浦波嵐", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_bar=auto_di, maai_list=dima_di(0, 10), kirihuda=True, flair=int_di(3),
    syuutan=True, taiou=True, taiounize=lambda c, d, h: papl_kougeki(c, d, h, -2, 0))

_cond_s_3: BoolDIIC = lambda delivery, call_h, cf_h, card: mine_cf(delivery, call_h, cf_h, card) and kessi(delivery, cf_h)

_cfs_s_3 = saiki_trigger(cls=Card, file_name="cards/na_01_yurina_o_s_3_s2.png",
            name="浮舟宿", cond=_cond_s_3, trigger=TG_1_OR_MORE_DAMAGE)

s_3 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_s_3_s2.png"), name="浮舟宿", cond=auto_di, type=CT_KOUDOU,
           kouka=Yazirusi(to_mine=True, to_code=UC_AURA, kazu=5).send, kirihuda=True, flair=int_di(2), used=[_cfs_s_3])

s_4 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_s_4.png"), name="天音揺波の底力", cond=kessi, type=CT_KOUGEKI,
    aura_damage_func=int_di(5), life_damage_func=int_di(5), maai_list=dima_di(1, 4), zenryoku=True, kirihuda=True, flair=int_di(5))
