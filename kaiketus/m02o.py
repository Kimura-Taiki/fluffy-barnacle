#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import MG_SAINE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
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

_cfs_n_5 = ScalarCorrection(name="圏域", cond=auto_diic, scalar=SC_TATUZIN, value=1)

n_5 = Card(megami=MG_SAINE, img=img_card("o_n_5_s5"), name="圏域", cond=auto_di, type=CT_HUYO,
           osame=int_di(2), amortize=_amortize_5, cfs=[_cfs_n_5])

_hakizi_n_6 = Card(megami=MG_SAINE, img=img_card("o_n_6_s3"), name="衝音晶：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_bar=auto_di, maai_list=dima_di(0, 10))

n_6 = Card(megami=MG_SAINE, img=img_card("o_n_6_s3"), name="衝音晶", cond=auto_di, type=CT_HUYO,
           osame=int_di(1), hakizi=_hakizi_n_6, taiou=True, taiounize=lambda c, d, h: papl_kougeki(c, d, h, -1, 0))

_cfs_n_7 = AuraGuard(name="無音壁", cond=auto_diic)

n_7 = Card(megami=MG_SAINE, img=img_card("o_n_7"), name="無音壁", cond=auto_di, type=CT_HUYO,
           osame=int_di(5), cfs=[_cfs_n_7], zenryoku=True)

_atk_s_1_1 = Card(megami=MG_SAINE, img=img_card("o_s_1_s2"), name="律動弧撃：序段", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

_atk_s_1_2 = Card(megami=MG_SAINE, img=img_card("o_s_1_s2"), name="律動弧撃：破段", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(4, 5))

_atk_s_1_3 = Card(megami=MG_SAINE, img=img_card("o_s_1_s2"), name="律動弧撃：急段", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(3, 5))

def _kouka_s_1(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="律動弧撃", delivery=delivery, hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _atk_s_1_1.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT1),
POP_ACT1: lambda l, s: _atk_s_1_2.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT2),
POP_ACT2: lambda l, s: _atk_s_1_3.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT3),
POP_ACT3: lambda l, s: moderator.pop()
    }))

s_1 = Card(megami=MG_SAINE, img=img_card("o_s_1_s2"), name="律動弧撃", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_s_1,
           kirihuda=True, flair=int_di(6))

_flair_s_2: SuuziDI = lambda delivery, hoyuusya: 8-delivery.ouka_count(hoyuusya=hoyuusya, is_mine=False, utuwa_code=UC_AURA)

s_2 = Card(megami=MG_SAINE, img=img_card("o_s_2_s2"), name="響鳴共振", cond=auto_di, type=CT_KOUDOU,
           kouka=Yazirusi(from_mine=False, from_code=UC_AURA, to_code=UC_MAAI, kazu=2).send,
           kirihuda=True, flair=_flair_s_2)

_cond_s_3: BoolDIIC = lambda delivery, call_h, cf_h, card: mine_cf(delivery, call_h, cf_h, card) and\
    hassou(delivery=delivery, hoyuusya=cf_h)

_cfs_s_3 = saiki_trigger(cls=Card, img=img_card("o_s_3_s6_2"),
            name="音無砕氷", cond=_cond_s_3, trigger=TG_END_PHASE)

s_3 = Card(megami=MG_SAINE, img=img_card("o_s_3_s6_2"), name="音無砕氷", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(0, 10),
    used=[_cfs_s_3], taiou=True, taiounize=lambda c, d, h: papl_kougeki(c, d, h, -1, -1), kirihuda=True, flair=int_di(2))

_cond_s_4: BoolDI = lambda delivery, hoyuusya: delivery.b_params.during_kirihuda

s_4 = Card(megami=MG_SAINE, img=img_card("o_s_4_s2"), name="氷雨細音の果ての果て", cond=_cond_s_4, type=CT_KOUGEKI,
    aura_damage_func=int_di(5), life_damage_func=int_di(5), maai_list=dima_di(1, 5),
    taiou=True, kirihuda=True, flair=int_di(5))
