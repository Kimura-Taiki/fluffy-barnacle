#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import enforce, opponent, MG_OBORO, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, TG_END_PHASE,\
    SC_SMOKE, SC_UROUO_YAZIRUSI, SC_UROUO_SETTI, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, OBAL_USE_CARD,\
    USAGE_USED, USAGE_UNUSED
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI, BoolDIC, nega_dic
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.ol.pop_stat import PopStat
from mod.ol.choice import choice_layer
from mod.ol.use_card_layer import use_card_layer
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.saikousei import saikousei_card
from mod.card.kw.yazirusi import Yazirusi, ya_ridatu
from mod.coous.saiki import saiki_trigger
from mod.coous.scalar_correction import ScalarCorrection
from mod.coous.aura_guard import AuraGuard
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer, NO_CHOICE
from mod.card.kw.handraw import handraw
from mod.card.kw.syuutyuu import isyuku, full_syuutyuu, reduce_syuutyuu
from mod.card.kw.handraw import handraw_card
from mod.card.kw.discard import discard_card
from mod.card.kw.setti import setti_layer

_ADDRESS = "na_05_oboro"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

n_1 = Card(megami=MG_OBORO, img=img_card("o_n_1"), name="鋼糸", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(3, 4), setti=True)

_cond_n_2: BoolDI = lambda delivery, hoyuusya: delivery.m_params(hoyuusya).use_from_husehuda

def _sutecard_n_2(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if stat.huda:
        huda = enforce(stat.huda, Huda).base
        layer.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)
    layer.moderate(PopStat(code))

def _kouka_n_2(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("相手々札の破棄", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "破棄手札の選択",
            lower=delivery.taba(opponent(hoyuusya), TC_TEHUDA), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _sutecard_n_2(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

_after_n_2 = TempKoudou("影菱：攻撃後", cond=_cond_n_2, kouka=_kouka_n_2)

n_2 = Card(megami=MG_OBORO, img=img_card("o_n_2_s2"), name="影菱", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(2, 2), taiouble=nega_dic,
    after=_after_n_2, setti=True)

def _aura_damage_3(delivery: Delivery, hoyuusya: int) -> int:
    return 4 if delivery.m_params(opponent(hoyuusya)).aura_damaged else 3

def _life_damage_3(delivery: Delivery, hoyuusya: int) -> int:
    return 3 if delivery.m_params(opponent(hoyuusya)).aura_damaged else 2

n_3 = Card(megami=MG_OBORO, img=img_card("o_n_3"), name="斬撃乱舞", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=_aura_damage_3, life_damage_func=_life_damage_3, maai_list=dima_di(2, 4), zenryoku=True)

_cond_n_4: BoolDI = lambda delivery, hoyuusya: not delivery.m_params(hoyuusya).ninpo_used

def _ninpo_use_n_4(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if layer.delivery.m_params(layer.hoyuusya).use_from_husehuda:
        layer.delivery.m_params(layer.hoyuusya).ninpo_used = True
        moderator.append(setti_layer(layer, stat, code))
    else:
        layer.moderate(PopStat(code))

def _ninpo_off_n_4(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.m_params(layer.hoyuusya).ninpo_used = False
    layer.moderate(PopStat(code))

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("忍歩", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: TempKoudou("離脱", auto_di, yazirusi=Yazirusi(
            to_code=UC_MAAI)).kaiketu(delivery, hoyuusya, code=POP_ACT1),
        POP_ACT1: lambda l, s: _ninpo_use_n_4(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _ninpo_off_n_4(l, s, POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

n_4 = Card(megami=MG_OBORO, img=img_card("o_n_4_s3"), name="忍歩", cond=_cond_n_4, type=CT_KOUDOU,
    kouka=_kouka_n_4, setti=True)

_tk_n_5_1 = TempKoudou(name="前進", cond=auto_di, yazirusi=Yazirusi(
    from_code=UC_MAAI, to_mine=False, to_code=UC_AURA))
_tk_n_5_2 = TempKoudou(name="宿し", cond=auto_di, yazirusi=Yazirusi(
    from_mine=False, from_code=UC_AURA, to_mine=False, to_code=UC_FLAIR))

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(over_layer=choice_layer(cards=[_tk_n_5_1, _tk_n_5_2], delivery=delivery, hoyuusya=hoyuusya))

n_5 = Card(megami=MG_OBORO, img=img_card("o_n_5"), name="誘導", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_5, taiou=True, setti=True)

def _hudas_n_6(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    li: list[Huda] = []
    for huda in delivery.taba(hoyuusya, TC_HUSEHUDA):
        if not enforce(huda, Huda).card.zenryoku:
            li.append(huda)
    return li

def _bunsin_card(huda: Huda) -> Card:
    card = copy(huda.card)
    if card.type == CT_KOUGEKI:
        card.taiouble = nega_dic
    return card

def _bunsin1_n_6(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if not stat.huda:
        layer.huda = None
        layer.moderate(PopStat(code))
        return
    huda = enforce(stat.huda, Huda).base
    layer.huda = huda
    card = _bunsin_card(huda=huda)
    layer.delivery.m_params(layer.hoyuusya).use_from_husehuda = True
    moderator.append(use_card_layer(cards=[card], name=f"{card.name}：分身１", youso=huda, mode=OBAL_USE_CARD, code=code))

def _bunsin2_n_6(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if not layer.huda:
        layer.moderate(PopStat(code))
        return
    huda = enforce(layer.huda, Huda).base
    if not huda in layer.delivery.taba(layer.hoyuusya, TC_SUTEHUDA):
        layer.moderate(PopStat(code))
        return
    card = _bunsin_card(huda=huda)
    layer.delivery.m_params(layer.hoyuusya).use_from_husehuda = True
    moderator.append(use_card_layer(cards=[card], name=f"{card.name}：分身２", youso=huda, mode=OBAL_USE_CARD, code=code))

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("分身の術", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "分身する伏せ札の選択",
            lower=_hudas_n_6(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _bunsin1_n_6(l ,s, POP_ACT2),
        POP_ACT2: lambda l, s: _ninpo_off_n_4(l, s, POP_ACT3),
        POP_ACT3: lambda l, s: _bunsin2_n_6(l, s, POP_ACT4),
        POP_ACT4: lambda l, s: _ninpo_off_n_4(l, s, POP_ACT5),
        POP_ACT5: lambda l, s: moderator.pop()
    }))

n_6 = Card(megami=MG_OBORO, img=img_card("o_n_6"), name="分身の術", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_6, zenryoku=True)

def _hudas_n_7(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, TC_KIRIHUDA)\
            if isinstance(huda, Huda) and huda.usage == USAGE_USED]

def _unusenize_n_7(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    enforce(stat.huda, Huda).base.usage = USAGE_UNUSED
    layer.moderate(PopStat(code))

def _kouka_n_7(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("生体活性", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "未使用に戻す切り札の選択",
            lower=_hudas_n_7(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _unusenize_n_7(l ,s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

_hakizi_n_7 = TempKoudou("生体活性：破棄時", auto_di, _kouka_n_7)

n_7 = suki_card(megami=MG_OBORO, img=img_card("o_n_7"), name="生体活性", cond=auto_di,
                osame=int_di(4), hakizi=_hakizi_n_7, setti=True)

def _count_s_1(layer: PipelineLayer, stat: PopStat, kuma_code: int, end_code: int) -> None:
    layer.mode += 1
    layer.moderate(PopStat(
        kuma_code if layer.mode <= len(layer.delivery.taba(layer.hoyuusya, TC_HUSEHUDA)) else end_code
    ))

_kuma_s_1 = Card(megami=MG_OBORO, img=img_card("o_s_1"), name="熊介：分身", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(3, 4), kirihuda=True)

def _kouka_s_1(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("熊介", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _count_s_1(l, s, POP_ACT1, POP_ACT2),
        POP_ACT1: lambda l, s: _kuma_s_1.kaiketu(delivery, hoyuusya, code=POP_OPEN),
        POP_ACT2: lambda l, s: moderator.pop()
    }, mode=0))

_after_s_1 = TempKoudou(name="熊介：攻撃後", cond=auto_di, kouka=_kouka_s_1)

s_1 = Card(megami=MG_OBORO, img=img_card("o_s_1"), name="熊介", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(3, 4),
    after=_after_s_1, zenryoku=True, kirihuda=True, flair=int_di(4))

def _tobikage_s_2(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    print(stat, stat.huda)
    if stat.huda:
        layer.delivery.m_params(layer.hoyuusya).use_from_husehuda = True
        enforce(stat.huda, Huda).card.kaiketu(layer.delivery, layer.hoyuusya, code=code)
    else:
        layer.moderate(PopStat(code))

def _stat_reset_s_2(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.m_params(layer.hoyuusya).use_from_husehuda = False
    layer.huda = stat.huda
    layer.moderate(PopStat(code))

def _kouka_s_2(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("鳶影", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "使用する伏せ札の選択",
            lower=_hudas_n_6(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _tobikage_s_2(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _stat_reset_s_2(l ,s, POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

s_2 = Card(megami=MG_OBORO, img=img_card("o_s_2_s3"), name="鳶影", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_2, taiou=True, kirihuda=True, flair=int_di(4))

def _hudas_s_3(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    taba: list[Huda] = delivery.taba(hoyuusya, TC_SUTEHUDA)
    return taba

def _branch_s_3(layer: PipelineLayer, stat: PopStat, huse_code: int, end_code: int) -> None:
    if enforce(stat.huda, Huda).card.name == "何もしない":
        layer.moderate(PopStat(end_code))
    else:
        layer.moderate(PopStat(code=huse_code, huda=stat.huda))

def _husecard_s_3(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_HUSEHUDA)
    layer.moderate(PopStat(code))

def _kouka_s_3(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("虚魚", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "伏せる捨て札の選択",
            lower=_hudas_s_3(delivery, hoyuusya), upper=[NO_CHOICE], code=POP_ACT1)),
        POP_ACT1: lambda l, s: _branch_s_3(l, s, POP_ACT2, POP_ACT3),
        POP_ACT2: lambda l, s: _husecard_s_3(l, s, POP_OPEN),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

_tenkaizi_s_3 = TempKoudou("虚魚：展開時", auto_di, _kouka_s_3)

_cfs_s_3_1 = ScalarCorrection(name="虚魚：展開中両矢印", cond=auto_diic, scalar=SC_UROUO_YAZIRUSI, value=1)
_cfs_s_3_2 = ScalarCorrection(name="虚魚：展開後再構成設置追加", cond=auto_diic, scalar=SC_UROUO_SETTI, value=1)

s_3 = Card(megami=MG_OBORO, img=img_card("o_s_3_s8_2"), name="虚魚", cond=auto_di, type=CT_HUYO,
           osame=int_di(3), tenkaizi=_tenkaizi_s_3, cfs=[_cfs_s_3_1, _cfs_s_3_2], used=[_cfs_s_3_2],
           kirihuda=True, flair=int_di(2))
