#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import enforce, opponent, MG_YUKIHI, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, TG_END_PHASE,\
    SC_DORORIURA, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, OBAL_USE_CARD,\
    USAGE_USED, USAGE_UNUSED
from mod.classes import Callable, Card, Huda, Delivery, moderator, popup_message
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI, MaaiDI, BoolDIC, nega_dic
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
from mod.coous.scalar_correction import ScalarCorrection, applied_scalar
from mod.coous.aura_guard import AuraGuard
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer, NO_CHOICE
from mod.card.kw.handraw import handraw
from mod.card.kw.syuutyuu import isyuku, full_syuutyuu, reduce_syuutyuu
from mod.card.kw.handraw import handraw_card
from mod.card.kw.discard import discard_card
from mod.card.kw.setti import setti_layer
from mod.card.kw.kasa_kaihei import kasa_kaihei_layer

_ADDRESS = "na_06_yukihi"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def logical_or_lists(li_1: list[bool], li_2: list[bool]) -> list[bool]:
    return [a or b for a, b in zip(li_1, li_2)]

_maai_n_1_ura: MaaiDI = lambda delivery, hoyuusya: dima_di(0, 2)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

_maai_n_1_omote: MaaiDI = lambda delivery, hoyuusya: dima_di(4, 6)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

_n_1_ura = Card(megami=MG_YUKIHI, img=img_card("o_n_1"), name="ふくみばり", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(2), maai_list=_maai_n_1_ura)

n_1 = Card(megami=MG_YUKIHI, img=img_card("o_n_1"), name="しこみばり", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=_maai_n_1_omote, henbou=True, horobi=_n_1_ura)

_maai_n_2_ura: MaaiDI = lambda delivery, hoyuusya: dima_di(0, 1)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 1)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

_maai_n_2_omote: MaaiDI = lambda delivery, hoyuusya: dima_di(4, 6)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 1)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

def _kouka_n_2(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(kasa_kaihei_layer(delivery, hoyuusya, POP_OK))

_after_n_2 = TempKoudou("しこねこ：攻撃後", auto_di, kouka=_kouka_n_2)

_n_2_ura = Card(megami=MG_YUKIHI, img=img_card("o_n_2_s8_2"), name="ねこだまし", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=_maai_n_2_ura, after=_after_n_2)

n_2 = Card(megami=MG_YUKIHI, img=img_card("o_n_2_s8_2"), name="しこみび", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=_maai_n_2_omote, after=_after_n_2,
    henbou=True, horobi=_n_2_ura)

_maai_n_3_ura: MaaiDI = lambda delivery, hoyuusya: dima_di(0, 2)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(2, 5)(delivery, hoyuusya))

_maai_n_3_omote: MaaiDI = lambda delivery, hoyuusya: dima_di(2, 5)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(2, 5)(delivery, hoyuusya))

_after_n_3_ura = TempKoudou("たぐりよせ：攻撃後", auto_di, yazirusi=Yazirusi(from_code=UC_MAAI, kazu=2))

_after_n_3_omote = TempKoudou("ふりはらい：攻撃後", auto_di, kouka=each_step)

_n_3_ura = Card(megami=MG_YUKIHI, img=img_card("o_n_3"), name="たぐりよせ", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=_maai_n_3_ura, after=_after_n_3_ura)

n_3 = Card(megami=MG_YUKIHI, img=img_card("o_n_3"), name="ふりはらい", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_damage_func=int_di(1), maai_list=_maai_n_3_omote, after=_after_n_3_omote,
    henbou=True, horobi=_n_3_ura)

_maai_n_4_ura: MaaiDI = lambda delivery, hoyuusya: dima_di(0, 2)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

_maai_n_4_omote: MaaiDI = lambda delivery, hoyuusya: dima_di(4, 6)(delivery, hoyuusya)\
    if applied_scalar(i=0, scalar=SC_DORORIURA, delivery=delivery) == 0 else\
    logical_or_lists(dima_di(0, 2)(delivery, hoyuusya), dima_di(4, 6)(delivery, hoyuusya))

_n_4_ura = Card(megami=MG_YUKIHI, img=img_card("o_n_4"), name="ふりまわし", cond=auto_di, type=CT_KOUGEKI,
    aura_bar=auto_di, life_damage_func=int_di(2), maai_list=_maai_n_4_ura, zenryoku=True)

n_4 = Card(megami=MG_YUKIHI, img=img_card("o_n_4"), name="つきさし", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(5), life_bar=auto_di, maai_list=_maai_n_4_omote, zenryoku=True,
    henbou=True, horobi=_n_4_ura)

n_5 = Card(megami=MG_YUKIHI, img=img_card("o_n_5"), name="かさまわし", cond=auto_di, type=CT_KOUDOU,
    kouka=lambda d, h: popup_message.add("かさまわしは使っても効果がありません"))

