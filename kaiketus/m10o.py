#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy
import random

from mod.const import enforce, opponent,\
    MG_KURURU, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_DIV, CT_ZENRYOKU, CT_HUTEI,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_KAIHEI, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN,\
    POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, POP_ACT6, POP_ACT7, POP_ACT8, POP_ACT9,\
    TG_END_PHASE,\
    SC_MODULO, SC_REFLECTOR,\
    TC_MISIYOU, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, OBAL_USE_CARD,\
    USAGE_USED, USAGE_DEPLOYED, USAGE_UNUSED,\
    IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE
from mod.classes import Callable, Card, Huda, Delivery, moderator, popup_message
from mod.card.card import auto_di, nega_di, int_di, dima_di, BoolDI, SuuziDI, MaaiDI, TaiounizeDI, BoolDIC, nega_dic
from mod.card.temp_koudou import TempKoudou
from mod.card.damage import Damage
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, enemy_cf, BoolDIIC, auto_diic
from mod.ol.pop_stat import PopStat
from mod.ol.choice import choice_layer
from mod.ol.use_card_layer import use_card_layer
from mod.ol.use_hand_layer import use_hand_layer
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

_ADDRESS = "na_10_kururu"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def _kikou_taba(delivery: Delivery, hoyuusya: int, taba_code: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, taba_code) if isinstance(huda, Huda) and\
            (True if taba_code == TC_SUTEHUDA else huda.usage != USAGE_UNUSED)]

def _type_count(delivery: Delivery, hoyuusya: int, type: int, taba_code: int) -> int:
    if type == CT_ZENRYOKU:
        return sum(1 for huda in _kikou_taba(delivery, hoyuusya, taba_code) if isinstance(huda, Huda) and huda.card.zenryoku)
    elif type == CT_TAIOU:
        return sum(1 for huda in _kikou_taba(delivery, hoyuusya, taba_code) if isinstance(huda, Huda) and huda.card.taiou)
    else:
        return sum(1 for huda in _kikou_taba(delivery, hoyuusya, taba_code) if isinstance(huda, Huda) and huda.card.type == type)

def _kikou_count(delivery: Delivery, hoyuusya: int, type: int) -> int:
    return _type_count(delivery, hoyuusya, type, TC_SUTEHUDA)+_type_count(delivery, hoyuusya, type, TC_KIRIHUDA)

def kikou(red: int=0, blue: int=0, green: int=0, purple: int=0, yellow: int=0) -> Callable[[Delivery, int], bool]:
    def _func(delivery: Delivery, hoyuusya: int) -> bool:
        li: list[tuple[int, int]] = [(red, CT_KOUGEKI), (blue, CT_KOUDOU),
            (green, CT_HUYO), (yellow, CT_ZENRYOKU), (purple, CT_TAIOU)]
        for mana, type in li:
            print(f"req{mana}, mana{_kikou_count(delivery, hoyuusya, type)}")
            if mana > 0 and mana > _kikou_count(delivery, hoyuusya, type):
                return False
        return True
    return _func

_direct_1life_damage = Damage(img=IMG_LIFE_DAMAGE, name="ライフに１ダメージ", dmg=1, from_code=UC_LIFE, to_code=UC_FLAIR)
_direct_5aura_damage = Damage(img=IMG_AURA_DAMAGE, name="オーラに５ダメージ", dmg=1, from_code=UC_AURA, to_code=UC_DUST)

def _kouka_n_1(delivery: Delivery, hoyuusya: int) -> None:
    if kikou(blue=3, purple=2)(delivery, hoyuusya):
        _direct_1life_damage.kaiketu(delivery, hoyuusya)

n_1 = Card(megami=MG_KURURU, img=img_card("o_n_1"), name="えれきてる", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_1)

def _on_accelr(layer: PipelineLayer, stat: PopStat, kikou_code: int, end_code: int) -> None:
    if kikou(blue=2, green=1)(layer.delivery, layer.hoyuusya):
        layer.delivery.m_params(layer.hoyuusya).during_accelr = True
        layer.moderate(PopStat(kikou_code))
    else:
        layer.moderate(PopStat(end_code))

def _hudas_n_2(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, TC_TEHUDA) if isinstance(huda, Huda) and huda.card.name != "あくせらー"]

def _off_accelr(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.m_params(layer.hoyuusya).during_accelr = False
    layer.moderate(PopStat(code))

def _kouka_n_2(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("あくせらー", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _on_accelr(l, s, POP_ACT1, POP_ACT4),
        POP_ACT1: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "使う手札を選択",
            lower=_hudas_n_2(delivery, hoyuusya), code=POP_ACT2)),
        POP_ACT2: lambda l, s: moderator.append(use_hand_layer("あくせらー経由の手札使用",
            card=enforce(enforce(s.huda, Huda).card, Card), huda=enforce(s.huda, Huda), code=POP_ACT3)),
        POP_ACT3: lambda l, s: _off_accelr(l, s, POP_ACT4),
        POP_ACT4: lambda l, s: moderator.pop()
        }))

n_2 = Card(megami=MG_KURURU, img=img_card("o_n_2"), name="あくせらー", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_2)

_cond_n_3: BoolDI = lambda delivery, hoyuusya: delivery.b_params.during_kougeki

def _hudas_transmigrate_n_3(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, TC_HUSEHUDA) if isinstance(huda, Huda)]

def _cmd_transmigrate_n_3(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_YAMAHUDA)
    layer.moderate(PopStat(code))

_transmigrate_n_3 = TempKoudou("伏せ札転生", auto_di, kouka=lambda d, h: moderator.append(PipelineLayer(
    name="伏せ札転生", delivery=d, hoyuusya=h, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(
            delivery=d, hoyuusya=h, name="山札に転生する伏せ札の選択",
            lower=_hudas_transmigrate_n_3(d, h), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _cmd_transmigrate_n_3(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    })))

def _hudas_sutecard_n_3(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [huda for huda in delivery.taba(hoyuusya, TC_TEHUDA) if isinstance(huda, Huda)]

def _cmd_sutecard_n_3(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_SUTEHUDA)
    layer.moderate(PopStat(code))

_sutecard_n_3 = TempKoudou("手札を捨てさせる", auto_di, kouka=lambda d, h: moderator.append(PipelineLayer(
     name="相手が手札を捨てる", delivery=d, hoyuusya=opponent(h), gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(
            delivery=d, hoyuusya=opponent(h), name="捨てる手札の選択",
            lower=_hudas_sutecard_n_3(d, opponent(h)), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _cmd_sutecard_n_3(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
     })))

def _cards_n_3(delivery: Delivery, hoyuusya: int) -> list[Card]:
    return [handraw_card, _transmigrate_n_3, _sutecard_n_3]

def _first_n_3(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.rest = stat.rest_taba
    enforce(stat.huda, Huda).card.kaiketu(layer.delivery, layer.hoyuusya, code=code)

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("くるるーん", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(
            delivery=delivery, hoyuusya=hoyuusya, name="くるるーん第１対応行動の選択",
            lower=_cards_n_3(delivery, hoyuusya), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _first_n_3(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.append(OnlySelectLayer(
            delivery=delivery, hoyuusya=hoyuusya, name="くるるーん第２対応行動の選択",
            lower=l.rest, code=POP_ACT3)),
        POP_ACT3: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT4),
        POP_ACT4: lambda l, s: moderator.pop()
    }))

n_3 = Card(megami=MG_KURURU, img=img_card("o_n_3"), name="くるるーん", cond=_cond_n_3, type=CT_KOUDOU,
    kouka=_kouka_n_3, taiou=True)

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("とるねーど", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: l.moderate(PopStat(POP_ACT1 if kikou(red=2)(delivery, hoyuusya) else POP_ACT2)),
        POP_ACT1: lambda l, s: _direct_5aura_damage.kaiketu(delivery, hoyuusya, code=POP_ACT2),
        POP_ACT2: lambda l, s: l.moderate(PopStat(POP_ACT3 if kikou(green=2)(delivery, hoyuusya) else POP_ACT4)),
        POP_ACT3: lambda l, s: _direct_1life_damage.kaiketu(delivery, hoyuusya, code=POP_ACT4),
        POP_ACT4: lambda l, s: moderator.pop()
    }))

n_4 = Card(megami=MG_KURURU, img=img_card("o_n_4"), name="とるねーど", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_4, zenryoku=True)

def _redshift_n_5(card: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(card)
    def maai_list(delivery: Delivery, hoyuusya: int) -> list[bool]:
        li = card.maai_list(delivery, hoyuusya)
        return [False]+li[0:10]
    taiounized.maai_list = maai_list
    return taiounized

def _blueshift_n_5(card: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(card)
    def maai_list(delivery: Delivery, hoyuusya: int) -> list[bool]:
        li = card.maai_list(delivery, hoyuusya)
        return li[1:11]+[False]
    taiounized.maai_list = maai_list
    return taiounized

_ad_plus_n_5: TaiounizeDI = lambda c, d, h: papl_kougeki(c, d, h, 1, 0)
_ad_minus_n_5: TaiounizeDI = lambda c, d, h: papl_kougeki(c, d, h, -1, 0)
_ld_plus_n_5: TaiounizeDI = lambda c, d, h: papl_kougeki(c, d, h, 0, 1)
_ld_minus_n_5: TaiounizeDI = lambda c, d, h: papl_kougeki(c, d, h, 0, -1)

def _osame_plus_n_5(card: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(card)
    def osame(delivery: Delivery, hoyuusya: int) -> int:
        return card.osame(delivery, hoyuusya)+1
    taiounized.osame = osame
    return taiounized

def _osame_minus_n_5(card: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(card)
    def osame(delivery: Delivery, hoyuusya: int) -> int:
        return card.osame(delivery, hoyuusya)-1
    taiounized.osame = osame
    return taiounized

def _pass_n_5(card: Card, delivery: Delivery, hoyuusya: int) -> Card:
    return card

_rs_card_n_5 = TempKoudou("赤方偏移", auto_di, kouka=lambda d, h: None, todo=[["適正距離の全ての値を+1"]])
_rs_card_n_5.taiounize = _redshift_n_5
_bs_card_n_5 = TempKoudou("青方偏移", auto_di, kouka=lambda d, h: None, todo=[["適正距離の全ての値を-1"]])
_bs_card_n_5.taiounize = _blueshift_n_5
_adp_card_n_5 = TempKoudou("オーラ＋１", auto_di, kouka=lambda d, h: None, todo=[["+1/0修正"]])
_adp_card_n_5.taiounize = _ad_plus_n_5
_adm_card_n_5 = TempKoudou("オーラ−１", auto_di, kouka=lambda d, h: None, todo=[["-1/0修正"]])
_adm_card_n_5.taiounize = _ad_minus_n_5
_ldp_card_n_5 = TempKoudou("ライフ＋１", auto_di, kouka=lambda d, h: None, todo=[["0/+1修正"]])
_ldp_card_n_5.taiounize = _ld_plus_n_5
_ldm_card_n_5 = TempKoudou("ライフ−１", auto_di, kouka=lambda d, h: None, todo=[["0/-1修正"]])
_ldm_card_n_5.taiounize = _ld_minus_n_5
_op_card_n_5 = TempKoudou("納＋１", auto_di, kouka=lambda d, h: None, todo=[["納を+1"]])
_op_card_n_5.taiounize = _osame_plus_n_5
_om_card_n_5 = TempKoudou("納−１", auto_di, kouka=lambda d, h: None, todo=[["納を-1"]])
_om_card_n_5.taiounize = _osame_minus_n_5
_pass_card_n_5 = TempKoudou("そのまま", auto_di, kouka=lambda d, h: None, todo=[["カードを修正しない"]])
_pass_card_n_5.taiounize = _pass_n_5

def _hudas_n_5(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    husehuda = [huda for huda in delivery.taba(hoyuusya, TC_HUSEHUDA) if isinstance(huda, Huda)\
                and not huda.card.zenryoku and huda.card.megami != MG_KURURU]
    sutehuda = [huda for huda in delivery.taba(hoyuusya, TC_SUTEHUDA) if isinstance(huda, Huda)\
                and not huda.card.zenryoku and huda.card.megami != MG_KURURU and huda.usage != USAGE_DEPLOYED]
    kirihuda = [huda for huda in delivery.taba(hoyuusya, TC_KIRIHUDA) if isinstance(huda, Huda)\
                and not huda.card.zenryoku and huda.card.megami != MG_KURURU and huda.usage == USAGE_USED]
    return husehuda+sutehuda+kirihuda

def _branch_n_5(layer: PipelineLayer, stat: PopStat, red_code: int, blue_code: int, green_code: int) -> None:
    huda = enforce(stat.huda, Huda).base
    layer.huda, layer.card = huda, huda.card
    layer.moderate(PopStat(
        code={CT_KOUGEKI: red_code, CT_KOUDOU: blue_code, CT_HUYO: green_code}.get(huda.card.type, -1),
        huda=huda, card=huda.card
    ))

def _correct_n_5(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    taiou = enforce(stat.huda, Huda).card
    layer.card = enforce(stat.huda, Huda).card.taiounize(enforce(layer.card, Card), layer.delivery, layer.hoyuusya)
    layer.moderate(PopStat(code))

def _kougeki_correct_n_5(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    moderator.append(PipelineLayer("りげいなー：攻撃札の修正", layer.delivery, layer.hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(l.delivery, l.hoyuusya, "増減対象の選択",
            lower=[_rs_card_n_5, _bs_card_n_5, _adp_card_n_5, _adm_card_n_5, _ldp_card_n_5, _ldm_card_n_5],
            upper=[_pass_card_n_5], code=POP_ACT1)),
        POP_ACT1: lambda l, s: _correct_n_5(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }, card=layer.card, huda=layer.huda, code=code))

def _huyo_correct_n_5(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    moderator.append(PipelineLayer("りげいなー：付与札の修正", layer.delivery, layer.hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(l.delivery, l.hoyuusya, "増減対象の選択",
            lower=[_op_card_n_5, _om_card_n_5], upper=[_pass_card_n_5], code=POP_ACT1)),
        POP_ACT1: lambda l, s: _correct_n_5(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }, card=layer.card, huda=layer.huda, code=code))

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("りげいなー", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: l.moderate(PopStat(POP_ACT1 if kikou(green=1, purple=1)(delivery, hoyuusya) else POP_ACT4)),
        POP_ACT1: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya, "使用する札の選択",
            lower=_hudas_n_5(delivery, hoyuusya), code=POP_ACT2)),
        POP_ACT2: lambda l, s: _branch_n_5(l, s, POP_ACT3, POP_ACT5, POP_ACT4),
        POP_ACT3: lambda l, s: _kougeki_correct_n_5(l, s, POP_ACT5),
        POP_ACT4: lambda l, s: _huyo_correct_n_5(l, s, POP_ACT5),
        POP_ACT5: lambda l, s: moderator.append(use_hand_layer(
            "りげいなーで使用", enforce(s.card, Card), enforce(s.huda, Huda), POP_ACT6)),
        POP_ACT6: lambda l, s: moderator.pop()
    }))

n_5 = Card(megami=MG_KURURU, img=img_card("o_n_5_s7_2"), name="りげいなー", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_5, zenryoku=True)

_cfs_n_6 = ScalarCorrection(name="もじゅるー", cond=mine_cf, scalar=SC_MODULO, value=1)

n_6 = Card(megami=MG_KURURU, img=img_card("o_n_6"), name="もじゅるー", cond=auto_di, type=CT_HUYO,
    osame=int_di(3), cfs=[_cfs_n_6])

def _tenkaizi_kouka_n_7(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, to_huda=delivery.m_params(hoyuusya).tenkaizi_huda, kazu=4)

_tenkaizi_n_7 = TempKoudou("りふれくた：展開時", kikou(red=1, purple=1), kouka=_tenkaizi_kouka_n_7)

_cfs_n_7 = ScalarCorrection(name="りふれくた", cond=mine_cf, scalar=SC_REFLECTOR, value=1)

n_7 = Card(megami=MG_KURURU, img=img_card("o_n_7"), name="りふれくた", cond=auto_di, type=CT_HUYO,
    osame=int_di(0), tenkaizi=_tenkaizi_n_7, cfs=[_cfs_n_7])

def _kouka_s_1(delivery: Delivery, hoyuusya: int) -> None:
    ...

s_1 = Card(megami=MG_KURURU, img=img_card("o_s_1"), name="どれーんでびる", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_1, kirihuda=True, flair=int_di(2), taiou=True)

def _kouka_s_2(delivery: Delivery, hoyuusya: int) -> None:
    ...

s_2 = Card(megami=MG_KURURU, img=img_card("o_s_2_s2"), name="びっぐごーれむ", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_2, kirihuda=True, flair=int_di(4))

def _kouka_s_3_ex(delivery: Delivery, hoyuusya: int) -> None:
    ...

s_3_ex = Card(megami=MG_KURURU, img=img_card("o_s_3_ex1"), name="でゅーぷりぎあ", cond=auto_di, type=CT_HUTEI,
    kouka=_kouka_s_1)

def _kouka_s_3(delivery: Delivery, hoyuusya: int) -> None:
    ...

s_3 = Card(megami=MG_KURURU, img=img_card("o_s_3_s5"), name="いんだすとりあ", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_3, kirihuda=True, flair=int_di(1))

def _kouka_s_4(delivery: Delivery, hoyuusya: int) -> None:
    ...

s_4 = Card(megami=MG_KURURU, img=img_card("o_s_4"), name="神渉装置・枢式", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_s_4, kirihuda=True, flair=int_di(3))
