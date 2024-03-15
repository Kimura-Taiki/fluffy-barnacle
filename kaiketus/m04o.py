#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import enforce, opponent, MG_TOKOYO, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TG_END_PHASE,\
    SC_SMOKE, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI, BoolDIC
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.ol.pop_stat import PopStat
from mod.ol.choice import choice_layer
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.saikousei import saikousei_card
from mod.card.kw.yazirusi import Yazirusi, ya_ridatu
from mod.coous.saiki import saiki_trigger
from mod.coous.scalar_correction import ScalarCorrection
from mod.coous.aura_guard import AuraGuard
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.card.kw.handraw import handraw
from mod.card.kw.syuutyuu import isyuku, full_syuutyuu, reduce_syuutyuu
from mod.card.kw.handraw import handraw_card
from mod.card.kw.discard import discard_card

_ADDRESS = "na_04_tokoyo"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def kyouti(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_SYUUTYUU) >= 2

def _kouka_n_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.b_params.sukinagasi = True

_after_n_1 = TempKoudou(name="梳流し：攻撃後", cond=kyouti, kouka=_kouka_n_1)

n_1 = Card(megami=MG_TOKOYO, img=img_card("o_n_1_s2"), name="梳流し", cond=auto_di, type=CT_KOUGEKI,
    aura_bar=auto_di, life_damage_func=int_di(1), maai_list=dima_di(4, 4), after=_after_n_1)

def _taiounize_n_2(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    if not taiounized.kirihuda and kyouti(delivery=delivery, hoyuusya=opponent(hoyuusya)):
        taiounized.aura_bar = auto_di
        taiounized.life_bar = auto_di
        taiounized.after = None
    return taiounized

n_2 = Card(megami=MG_TOKOYO, img=img_card("o_n_2"), name="雅打ち", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(2, 4), taiou=True, taiounize=_taiounize_n_2)

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    if delivery.b_params.maai <= 3:
        Yazirusi(to_code=UC_MAAI, kazu=2).send(delivery=delivery, hoyuusya=hoyuusya)

n_3 = Card(megami=MG_TOKOYO, img=img_card("o_n_3"), name="跳ね兎", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_3)

_tk_n_4_1 = TempKoudou(name="捌き", cond=auto_di, yazirusi=Yazirusi(
    from_mine=True, from_code=UC_FLAIR, to_mine=True, to_code=UC_AURA))
_tk_n_4_2 = TempKoudou(name="後退", cond=auto_di, yazirusi=Yazirusi(from_mine=True, from_code=UC_AURA, to_code=UC_MAAI))

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(over_layer=choice_layer(cards=[_tk_n_4_1, _tk_n_4_2], delivery=delivery, hoyuusya=hoyuusya))

n_4 = Card(megami=MG_TOKOYO, img=img_card("o_n_4"), name="詩舞", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_4, taiou=True)

def _lower_n_5(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    husehuda = delivery.taba(hoyuusya=hoyuusya, taba_code=TC_HUSEHUDA)
    sutehuda = delivery.taba(hoyuusya=hoyuusya, taba_code=TC_SUTEHUDA)
    li: list[Huda] = husehuda+sutehuda
    return li

_upper_n_5 = Card(img=IMG_NO_CHOICE, name="何もしない", cond=auto_di, type=CT_KOUDOU)

def _os_layer_n_5(delivery: Delivery, hoyuusya: int, code: int) -> OnlySelectLayer:
    return OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya, name="還元する札の選択",
        lower=_lower_n_5(delivery=delivery, hoyuusya=hoyuusya), upper=[_upper_n_5], code=code)

def _kaiketu_n_5(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    huda = enforce(stat.huda, Huda)
    if huda.card.name != "何もしない":
        layer.delivery.send_huda_to_ryouiki(huda=huda.base, is_mine=True, taba_code=TC_YAMAHUDA)
    layer.moderate(PopStat(code))

def _pl_layer_n_5(delivery: Delivery, hoyuusya: int, code: int) -> PipelineLayer:
    return PipelineLayer(name="山札へ還元", delivery=delivery, hoyuusya=hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(_os_layer_n_5(delivery, hoyuusya, POP_ACT1)),
        POP_ACT1: lambda l, s: _kaiketu_n_5(layer=l, stat=s, code=POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }, code=code)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="要返し", delivery=delivery, hoyuusya=hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(_pl_layer_n_5(delivery, hoyuusya, POP_ACT1)),
        POP_ACT1: lambda l, s: moderator.append(_pl_layer_n_5(delivery, hoyuusya, POP_ACT2)),
        POP_ACT2: lambda l, s: TempKoudou(name="２纏い", cond=auto_di, yazirusi=Yazirusi(
            to_mine=True, to_code=UC_AURA, kazu=2)).kaiketu(delivery, hoyuusya, code=POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

n_5 = Card(megami=MG_TOKOYO, img=img_card("o_n_5"), name="要返し", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_5, zenryoku=True)

n_6 = Card(megami=MG_TOKOYO, img=img_card("o_n_6"), name="風舞台", cond=auto_di, type=CT_HUYO, osame=int_di(2),
    tenkaizi=TempKoudou(name="２前身", cond=auto_di, yazirusi=Yazirusi(from_code=UC_MAAI, to_mine=True, to_code=UC_AURA, kazu=2)),
    hakizi=TempKoudou(name="２後退", cond=auto_di, yazirusi=Yazirusi(from_mine=True, from_code=UC_AURA, to_code=UC_MAAI, kazu=2)))

n_7 = Card(megami=MG_TOKOYO, img=img_card("o_n_7_s6_2"), name="晴舞台", cond=auto_di, type=CT_HUYO, osame=int_di(2),
    tenkaizi=TempKoudou(name="集中２", cond=auto_di, kouka=full_syuutyuu),
    hakizi=Card(megami=MG_TOKOYO, img=img_card("o_n_7_s6_2"), name="晴舞台：破棄時", cond=auto_di, type=CT_KOUGEKI,
    aura_bar=auto_di, life_damage_func=int_di(1), maai_list=dima_di(3, 6)))

def _taiounize_s_1(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    taiounized.aura_bar = auto_di
    taiounized.life_bar = auto_di
    taiounized.after = None
    return taiounized

s_1 = Card(megami=MG_TOKOYO, img=img_card("o_s_1"), name="久遠ノ花", cond=auto_di, type=CT_KOUGEKI,
    aura_bar=auto_di, life_damage_func=int_di(1), maai_list=dima_di(0, 10),
    kirihuda=True, flair=int_di(5), taiou=True, taiounize=_taiounize_s_1)

s_2 = Card(megami=MG_TOKOYO, img=img_card("o_s_2"), name="千歳ノ鳥", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(3, 4),
    after=saikousei_card, kirihuda=True, flair=int_di(2))

def _hikougeki_tehuda(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    tehuda = delivery.taba_(hoyuusya=hoyuusya, taba_code=TC_TEHUDA)
    li: list[Huda] = []
    for huda in tehuda:
        if isinstance(huda, Huda) and huda.card.type != CT_KOUGEKI:
            li.append(huda)
    return li

def _sutecard(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_SUTEHUDA)
    layer.moderate(PopStat(code))

def _kouka_s_3(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="非攻撃札の破棄", delivery=delivery, hoyuusya=opponent(hoyuusya), gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, l.hoyuusya, name="捨てる非攻撃札を選択",
            lower=_hikougeki_tehuda(delivery, l.hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _sutecard(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

_after_s_3 = TempKoudou(name="無窮ノ風：攻撃後", cond=auto_di, kouka=_kouka_s_3)

_cond_s_3: BoolDIIC = lambda delivery, call_h, cf_h, card: mine_cf(delivery, call_h, cf_h, card) and\
    kyouti(delivery=delivery, hoyuusya=cf_h)

_cfs_s_3 = saiki_trigger(cls=Card, img=img_card("o_s_3_s2"),
            name="無窮ノ風", cond=_cond_s_3, trigger=TG_END_PHASE)

s_3 = Card(megami=MG_TOKOYO, img=img_card("o_s_3_s2"), name="無窮ノ風", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=dima_di(3, 8), after=_after_s_3,
    kirihuda=True, flair=int_di(1), cfs=[_cfs_s_3])

def _kouka_s_4(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="常世ノ月", delivery=delivery, hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: TempKoudou("集中２", auto_di, full_syuutyuu).kaiketu(delivery, hoyuusya, code=POP_ACT1),
POP_ACT1: lambda l, s: TempKoudou("相手集中０", auto_di, reduce_syuutyuu).kaiketu(delivery, opponent(hoyuusya), code=POP_ACT2),
POP_ACT2: lambda l, s: TempKoudou("畏縮", auto_di, isyuku).kaiketu(delivery, hoyuusya, code=POP_ACT3),
POP_ACT3: lambda l, s: moderator.pop()
    }))

s_4 = Card(megami=MG_TOKOYO, img=img_card("o_s_4"), name="常世ノ月", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_s_4,
           kirihuda=True, flair=int_di(2))


