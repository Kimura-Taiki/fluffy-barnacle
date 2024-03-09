#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import MG_SAINE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA, UC_DUST
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.ol.choice import choice_layer
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.yazirusi import Yazirusi, ya_ridatu
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

_after_n_3 = Card(megami=MG_SAINE, img=img_card("o_n_3_s6_2"), name="石突：攻撃後", cond=hassou, type=CT_KOUDOU,
    kouka=ya_ridatu.send, taiou=True)

n_3 = Card(megami=MG_SAINE, img=img_card("o_n_3_s6_2"), name="石突", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(2, 3), after=_after_n_3, taiou=True)

_cond_n_4: BoolDI = lambda delivery, hoyuusya: not delivery.b_params.during_kougeki or hassou(delivery, hoyuusya)

n_4 = Card(megami=MG_SAINE, img=img_card("o_n_4_s6_2"), name="見切り", cond=_cond_n_4, type=CT_KOUDOU, kouka=each_step,
           taiou=True)

def _amortize_5(huda: Huda) -> None:
    huda.delivery.send_ouka_to_ryouiki(hoyuusya=huda.hoyuusya, from_huda=huda, to_code=UC_MAAI)

n_5 = Card(megami=MG_SAINE, img=img_card("o_n_5_s5"), name="圏域", cond=auto_di, type=CT_HUYO,
           osame=int_di(2), amortize=_amortize_5)
