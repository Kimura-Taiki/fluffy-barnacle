#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import MG_SAINE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.delivery import Delivery
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.coous.saiki import saiki_trigger

_ADDRESS = "na_02_saine"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def hassou(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_AURA) <= 1

_after_n_1 = Card(megami=MG_SAINE, img=img_card("o_n_1_s6_2"), name="八方振り：攻撃後", cond=hassou, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(4, 5))

n_1 = Card(megami=MG_SAINE, img=img_card("o_n_1_s6_2"), name="八方振り", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(4, 5), after=_after_n_1)

n_2 = Card(megami=MG_SAINE, img=img_card("o_n_2"), name="薙斬り", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(4, 5), taiou=True)
