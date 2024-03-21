#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy
import random

from mod.const import enforce, opponent, MG_TIKAGE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_KAIHEI, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, TG_END_PHASE,\
    SC_MAAI, SC_TIKANDOKU, SC_TONZYUTU, SC_DEINEI,\
    TC_MISIYOU, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, OBAL_USE_CARD,\
    USAGE_USED, USAGE_UNUSED
from mod.classes import Callable, Card, Huda, Delivery, moderator, popup_message
from mod.card.card import auto_di, nega_di, int_di, dima_di, BoolDI, SuuziDI, MaaiDI, BoolDIC, nega_dic
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, enemy_cf, BoolDIIC, auto_diic
from mod.ol.pop_stat import PopStat
from mod.ol.choice import choice_layer
from mod.ol.use_card_layer import use_card_layer
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.saikousei import saikousei_card
from mod.card.kw.yazirusi import Yazirusi, ya_moguri, ya_ridatu, ya_koutai, ya_matoi
from mod.coous.saiki import saiki_trigger
from mod.coous.scalar_correction import ScalarCorrection, applied_scalar
from mod.coous.aura_guard import AuraGuard
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer, NO_CHOICE
from mod.card.kw.handraw import handraw
from mod.card.kw.syuutyuu import syuutyuu, isyuku, full_syuutyuu, reduce_syuutyuu, deprive_syuutyuu
from mod.card.kw.handraw import handraw_card
from mod.card.kw.discard import discard_card
from mod.card.kw.setti import setti_layer
from mod.card.kw.kasa_kaihei import kasa_kaihei_layer, kaihei_card

_ADDRESS = "na_09_chikage"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def _kaiki(delivery: Delivery, hoyuusya: int) -> None:
    huda = enforce(enforce(moderator.last_layer(), PipelineLayer).huda, Huda).base
    delivery.send_huda_to_ryouiki(huda=huda, is_mine=False, taba_code=TC_MISIYOU)

def _kaiki_huyo(delivery: Delivery, hoyuusya: int) -> None:
    huda = next(huda for huda in delivery.taba(hoyuusya, TC_SUTEHUDA) if enforce(huda, Huda).card.name == "弛緩毒")
    delivery.send_huda_to_ryouiki(huda=huda, is_mine=False, taba_code=TC_MISIYOU)

def _tanki_doku(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, TC_MISIYOU) if "tanki_doku" in enforce(huda, Huda).card.kwargs]

def _send_doku(layer: PipelineLayer, stat: PopStat, taba_code: int, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=False, taba_code=taba_code)
    layer.moderate(PopStat(code))

def _cond_p_1(delivery: Delivery, hoyuusya: int) -> bool:
    print("麻痺毒条件", delivery, hoyuusya)
    return not delivery.m_params(hoyuusya).played_standard

def _kouka_p_1(delivery: Delivery, hoyuusya: int) -> None:
    _kaiki(delivery, hoyuusya)
    delivery.b_params.phase_ended = True

p_1 = Card(megami=MG_TIKAGE, img=img_card("o_p_1"), name="麻痺毒", cond=_cond_p_1, type=CT_KOUDOU,
    kouka=_kouka_p_1, doku=True, tanki_doku=True, unhuseable=True)

def _kouka_p_2(delivery: Delivery, hoyuusya: int) -> None:
    _kaiki(delivery, hoyuusya)
    Yazirusi(from_mine=True, from_code=UC_FLAIR, kazu=2).send(delivery, hoyuusya)

p_2 = Card(megami=MG_TIKAGE, img=img_card("o_p_2"), name="幻覚毒", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_p_2,
    doku=True, tanki_doku=True, unhuseable=True)

_cfs_p_3 = ScalarCorrection(name="弛緩毒", cond=auto_diic, scalar=SC_TIKANDOKU, value=1)

_hakizi_p_3 = TempKoudou("弛緩毒：破棄時", auto_di, kouka=_kaiki_huyo)

p_3 = Card(megami=MG_TIKAGE, img=img_card("o_p_3"), name="弛緩毒", cond=auto_di, type=CT_HUYO,
    osame=int_di(3), hakizi=_hakizi_p_3, cfs=[_cfs_p_3], doku=True, tanki_doku=True, unhuseable=True)

p_4 = Card(megami=MG_TIKAGE, img=img_card("o_p_4"), name="滅灯毒", cond=auto_di, type=CT_KOUDOU,
    kouka=Yazirusi(from_mine=True, from_code=UC_AURA, kazu=3).send,
    doku=True, unhuseable=True)

n_1 = Card(megami=MG_TIKAGE, img=img_card("o_n_1"), name="飛苦無", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(4, 5))

def _kouka_n_2(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("毒を山札へ", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "山札へ送る毒の選択",
            lower=_tanki_doku(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _send_doku(l, s, TC_YAMAHUDA, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

_after_n_2 = TempKoudou("毒針：攻撃後", auto_di, _kouka_n_2)

n_2 = Card(megami=MG_TIKAGE, img=img_card("o_n_2"), name="毒針", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(4, 4), after=_after_n_2)

_cfs_n_3 = ScalarCorrection(name="遁術", cond=enemy_cf, scalar=SC_TONZYUTU, value=1)

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("遁術", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: TempKoudou("遁術：後退", auto_di, yazirusi=ya_koutai).kaiketu(delivery, hoyuusya, code=POP_ACT1),
        POP_ACT1: lambda l, s: TempKoudou("遁術：離脱", auto_di, yazirusi=ya_ridatu).kaiketu(delivery, hoyuusya, code=POP_ACT2),
        POP_ACT2: lambda l, s: TempKoudou("遁術：残存効果", auto_di, kouka=lambda d, h:\
            d.m_params(h).lingerings.append(_cfs_n_3)).kaiketu(delivery, hoyuusya, code=POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

_after_n_3 = TempKoudou("遁術：攻撃後", auto_di, kouka=_kouka_n_3)

n_3 = Card(megami=MG_TIKAGE, img=img_card("o_n_3_s5"), name="遁術", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_bar=auto_di, maai_list=dima_di(1, 3), after=_after_n_3)

def _kouka_n_4_matoi(delivery: Delivery, hoyuusya: int) -> None:
    if  any("doku" in enforce(huda, Huda).card.kwargs for huda in delivery.taba(opponent(hoyuusya), TC_TEHUDA)):
        ya_matoi.send(delivery, hoyuusya)

def _kouka_n_4_zenryoku(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("暗器：全力化", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, opponent(hoyuusya), name="受け取る毒の選択",
            lower=_tanki_doku(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _send_doku(l, s, TC_TEHUDA, POP_ACT2),
        POP_ACT2: lambda l, s: _after_n_4.kaiketu(delivery, hoyuusya, code=POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

_after_n_4 = TempKoudou("暗器：攻撃後", auto_di, kouka=_kouka_n_4_matoi)
_after_n_4_zenryoku = TempKoudou("暗器：全力化：攻撃後", auto_di, kouka=_kouka_n_4_zenryoku)

_n_4_zenryoku = Card(megami=MG_TIKAGE, img=img_card("o_n_4_s8_2"), name="暗器：全力化", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(3), maai_list=dima_di(1, 5), after=_after_n_4_zenryoku,
    zenryoku=True)

n_4 = Card(megami=MG_TIKAGE, img=img_card("o_n_4_s8_2"), name="暗器", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(1, 5), after=_after_n_4,
    taiou=True, zenryokuize=True, zenryokued=_n_4_zenryoku)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("毒を手札へ", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "手札へ送る毒の選択",
            lower=_tanki_doku(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _send_doku(l, s, TC_TEHUDA, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

n_5 = Card(megami=MG_TIKAGE, img=img_card("o_n_5"), name="毒霧", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_5)

n_6 = suki_card(megami=MG_TIKAGE, img=img_card("o_n_6"), name="抜き足", cond=auto_di,
    osame=int_di(4), hakizi=TempKoudou("スカ", auto_di, kouka=lambda d, h: None),
    cfs=[ScalarCorrection(name="抜き足", cond=auto_diic, scalar=SC_MAAI, value=-2)])

n_7 = Card(megami=MG_TIKAGE, img=img_card("o_n_7"), name="泥濘", cond=auto_di, type=CT_HUYO,
    osame=int_di(2), cfs=[ScalarCorrection(name="泥濘", cond=enemy_cf, scalar=SC_DEINEI, value=1)])

def _kouka_s_1(delivery: Delivery, hoyuusya: int) -> None:
    horobi_doku = next(huda for huda in delivery.taba(hoyuusya, TC_MISIYOU)\
        if isinstance(huda, Huda) and huda.card.name == "滅灯毒")
    delivery.send_huda_to_ryouiki(huda=horobi_doku, is_mine=False, taba_code=TC_YAMAHUDA, is_top=True)

s_1 = Card(megami=MG_TIKAGE, img=img_card("o_s_1"), name="滅灯の魂毒", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_1, kirihuda=True, flair=int_di(3))

def _taiounize_cfs_s_2(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    if kougeki.aura_bar(delivery, hoyuusya) or kougeki.life_bar(delivery, hoyuusya):
        taiounized.kwargs["utikesied"] = True
    return taiounized

def _taiounize_s_2(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    if kougeki.aura_bar(delivery, hoyuusya) or kougeki.life_bar(delivery, hoyuusya):
        taiounized.kwargs["utikesied"] = True
    return taiounized

s_2 = Card(megami=MG_TIKAGE, img=img_card("o_s_2"), name="叛旗の纏毒", cond=auto_di, type=CT_HUYO,
    osame=int_di(5), cfs=[AttackCorrection(name="叛旗の纏毒", cond=enemy_cf, taiounize=_taiounize_cfs_s_2)],
    taiou=True, taiounize=_taiounize_s_2, kirihuda=True, flair=int_di(2))

_cond_s_3: BoolDIIC = lambda delivery, call_h, cf_h, card: mine_cf(delivery, call_h, cf_h, card) and\
    len(delivery.taba(opponent(cf_h), TC_TEHUDA)) >= 2

_cfs_s_3 = saiki_trigger(cls=Card, img=img_card("o_s_3"),
            name="流転の霞毒", cond=_cond_s_3, trigger=TG_END_PHASE)

s_3 = Card(megami=MG_TIKAGE, img=img_card("o_s_3"), name="流転の霞毒", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(2), maai_list=dima_di(3, 7),
    used=[_cfs_s_3], kirihuda=True, flair=int_di(1))

s_4 = Card(megami=MG_TIKAGE, img=img_card("o_s_4"), name="闇昏千影の生きる道", cond=auto_di, type=CT_HUYO,
    osame=int_di(4), cfs=[],
    zenryoku=True, kirihuda=True, flair=int_di(5))

# def _taiounize_cfs_s_2(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
#     taiounized = copy(kougeki)
#     def taiouble(delivery: Delivery, hoyuusya: int, card: Card) -> bool:
#         return False if not card.kirihuda else kougeki.taiouble(delivery, hoyuusya, card)
#     def maai_list(delivery: Delivery, hoyuusya: int) -> list[bool]:
#         li = kougeki.maai_list(delivery, hoyuusya)
#         for i, v in enumerate(li):
#             if i == 0 or not v:
#                 continue
#             li[i-1] = True
#             break
#         return li
#     taiounized.taiouble = taiouble
#     taiounized.maai_list = maai_list
#     return taiounized

# _cond_n_5: BoolDIIC = lambda delivery, atk_h, cf_h, card: \
#     mine_cf(delivery, atk_h, cf_h, card) and card.megami != MG_YURINA and not card.kirihuda

# _cfs_n_5 = AttackCorrection(name="気迫", cond=enemy_cf, taiounize=_taiounize_cfs_s_2)
