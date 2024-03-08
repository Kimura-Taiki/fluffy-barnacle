#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import MG_SAINE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA, UC_DUST
from mod.classes import Card, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.ol.choice import choice_layer
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

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, to_mine=False, to_code=UC_MAAI)

_after_n_3 = Card(megami=MG_SAINE, img=img_card("o_n_3_s6_2"), name="石突：攻撃後", cond=hassou, type=CT_KOUDOU,
    kouka=_kouka_n_3, taiou=True)

n_3 = Card(megami=MG_SAINE, img=img_card("o_n_3_s6_2"), name="石突", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(2, 3), after=_after_n_3, taiou=True)

def _kouka_n_4_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_DUST, kazu=1)

def _kouka_n_4_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI, kazu=1)

tkn41 = TempKoudou(name="見切り：潜り", cond=auto_di, kouka=_kouka_n_4_1, todo=[[False, UC_MAAI, False, UC_DUST, 1]])
tkn42 = TempKoudou(name="見切り：離脱", cond=auto_di, kouka=_kouka_n_4_2, todo=[[False, UC_DUST, False, UC_MAAI, 1]])

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    moderator.append(over_layer=choice_layer(cards=[tkn41, tkn42], delivery=delivery, hoyuusya=hoyuusya))

_cond_n_4: BoolDI = lambda delivery, hoyuusya: not delivery.b_params.during_kougeki or hassou(delivery, hoyuusya)

n_4 = Card(megami=MG_SAINE, img=img_card("o_n_4_s6_2"), name="見切り", cond=_cond_n_4, type=CT_KOUDOU, kouka=_kouka_n_4,
           taiou=True)
