#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import MG_HIMIKA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA, UC_DUST, SC_TATUZIN, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TG_END_PHASE
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.ol.choice import choice_layer
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.yazirusi import Yazirusi, ya_ridatu
from mod.coous.saiki import saiki_trigger
from mod.coous.scalar_correction import ScalarCorrection
from mod.coous.aura_guard import AuraGuard
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.handraw import handraw
from mod.card.kw.syuutyuu import isyuku

_ADDRESS = "na_03_himika"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def renka(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.m_params(hoyuusya=hoyuusya).use_card_count >= 2

n_1 = Card(megami=MG_HIMIKA, img=img_card("o_n_1"), name="シュート", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(4, 10))

_ad_n_2: SuuziDI = lambda delivery, hoyuusya: 3 if renka(delivery, hoyuusya) else 2
_ld_n_2: SuuziDI = lambda delivery, hoyuusya: 2 if renka(delivery, hoyuusya) else 1

n_2 = Card(megami=MG_HIMIKA, img=img_card("o_n_2_s4"), name="ラピッドファイア", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_ad_n_2, life_damage_func=_ld_n_2, maai_list=dima_di(6, 8))

_after_n_3 = Card(megami=MG_HIMIKA, img=img_card("o_n_3"), name="マグナムカノン：攻撃後", cond=auto_di, type=CT_KOUDOU,
    kouka=Yazirusi(from_mine=True, from_code=UC_LIFE).send)

n_3 = Card(megami=MG_HIMIKA, img=img_card("o_n_3"), name="マグナムカノン", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(5, 8), after=_after_n_3)

n_4 = Card(megami=MG_HIMIKA, img=img_card("o_n_4"), name="フルバースト", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(5, 9), zenryoku=True,
    burst=True)

_part_n_5_1 = Card(megami=MG_HIMIKA, img=img_card("o_n_5"), name="バックステップ：ドロー", cond=auto_di, type=CT_KOUDOU,
    kouka=handraw)

_part_n_5_2 = Card(megami=MG_HIMIKA, img=img_card("o_n_5"), name="バックステップ：矢印離脱", cond=auto_di, type=CT_KOUDOU,
    kouka=ya_ridatu.send)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="バックステップ", delivery=delivery, hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _part_n_5_1.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT1),
POP_ACT1: lambda l, s: _part_n_5_2.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop()
    }))

n_5 = Card(megami=MG_HIMIKA, img=img_card("o_n_5"), name="バックステップ", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_5)

_cond_n_6: BoolDIIC = lambda delivery, atk_h, cf_h, card: mine_cf(delivery, atk_h, cf_h, card) and card.megami != MG_HIMIKA

_cfs_n_6 = AttackCorrection(name="バックドラフト", cond=_cond_n_6, taiounize=lambda c, d, h: papl_attack(c, d, h, 1, 1))

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    isyuku(delivery=delivery,hoyuusya=hoyuusya)
    if renka(delivery=delivery, hoyuusya=hoyuusya):
        delivery.m_params(hoyuusya).lingerings.append(_cfs_n_6)

n_6 = Card(megami=MG_HIMIKA, img=img_card("o_n_6_s5"), name="バックドラフト", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_6)
