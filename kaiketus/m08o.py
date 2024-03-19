#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy
import random

from mod.const import enforce, opponent, MG_HAGANE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_KAIHEI, IMG_NO_CHOICE,\
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
from mod.card.kw.yazirusi import Yazirusi, ya_moguri, ya_ridatu, ya_matoi
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

_ADDRESS = "na_08_hagane"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def ensin(delivery: Delivery, hoyuusya: int) -> bool:
    if delivery.m_params(hoyuusya).played_kougeki:
        popup_message.add("遠心は攻撃済みだと達成できません")
        return False
    return delivery.b_params.maai >= delivery.b_params.start_turn_maai+2

def _discard_n_1(delivery: Delivery, hoyuusya: int, is_mine: bool, code: int) -> None:
    for huda in list(delivery.taba(hoyuusya=hoyuusya if is_mine else opponent(hoyuusya), taba_code=TC_TEHUDA)):
        delivery.send_huda_to_ryouiki(huda=enforce(huda, Huda), is_mine=True, taba_code=TC_HUSEHUDA)
    moderator.last_layer().moderate(PopStat(code))

def _reduce_and_phase_end_n_1(delivery: Delivery, hoyuusya: int, code: int) -> None:
    reduce_syuutyuu(delivery, hoyuusya)
    delivery.b_params.phase_ended = True
    moderator.last_layer().moderate(PopStat(code))

def _kouka_n_1(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("遠心撃：自ターン攻撃後", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _discard_n_1(delivery, hoyuusya, True, POP_ACT1),
        POP_ACT1: lambda l, s: _discard_n_1(delivery, hoyuusya, False, POP_ACT2),
        POP_ACT2: lambda l, s: _reduce_and_phase_end_n_1(delivery, hoyuusya, POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

_cond_n_1: BoolDI = lambda delivery, hoyuusya: delivery.turn_player == moderator.last_layer().hoyuusya
_after_n_1 = TempKoudou("遠心撃：攻撃後", _cond_n_1, kouka=_kouka_n_1)

n_1 = Card(megami=MG_HAGANE, img=img_card("o_n_1_s2"), name="遠心撃", cond=ensin, type=CT_KOUGEKI,
    aura_damage_func=int_di(5), life_damage_func=int_di(3), maai_list=dima_di(2, 6), after=_after_n_1)

def _kouka_n_2(delivery: Delivery, hoyuusya: int) -> None:
    tehuda: list[Huda] = delivery.taba(opponent(hoyuusya), TC_TEHUDA)
    delivery.send_huda_to_ryouiki(huda=random.choice(tehuda), is_mine=True, taba_code=TC_SUTEHUDA)

_cond_n_2: BoolDI = lambda delivery, hoyuusya: abs(delivery.b_params.start_turn_maai-delivery.b_params.maai) >= 2
_after_n_2 = TempKoudou("砂風塵：攻撃後", _cond_n_2, kouka=_kouka_n_2)

n_2 = Card(megami=MG_HAGANE, img=img_card("o_n_2"), name="砂風塵", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(1), life_bar=auto_di, maai_list=dima_di(0, 6), after=_after_n_2)

def _kouka_n_3(delivery: Delivery, hoyuusya: int) -> None:
    deprive_syuutyuu(delivery, hoyuusya)
    isyuku(delivery, hoyuusya)

_after_n_3 = TempKoudou("大地砕き：攻撃後", auto_di, kouka=_kouka_n_3)

n_3 = Card(megami=MG_HAGANE, img=img_card("o_n_3"), name="大地砕き", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_bar=auto_di, maai_list=dima_di(0, 3), taiouble=nega_dic, after=_after_n_3, zenryoku=True)

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    (Yazirusi(from_code=UC_MAAI, to_mine=True, to_code=UC_FLAIR)
     if delivery.b_params.maai >= 5
     else Yazirusi(from_code=UC_FLAIR, to_code=UC_MAAI)).send(delivery, hoyuusya)

n_4 = Card(megami=MG_HAGANE, img=img_card("o_n_4_s6_2"), name="超反動", cond=auto_di, type=CT_KOUDOU,
    kouka=_kouka_n_4)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    if delivery.ouka_count(hoyuusya, False, UC_FLAIR) >= 3:
        Yazirusi(from_code=UC_FLAIR, to_mine=True, to_code=UC_AURA, kazu=2).send(delivery, hoyuusya)

n_5 = Card(megami=MG_HAGANE, img=img_card("o_n_5"), name="円舞錬", cond=ensin, type=CT_KOUDOU,
    kouka=_kouka_n_5)

def _taiounize_cfs_n_6_2(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def maai_list(delivery: Delivery, hoyuusya: int) -> list[bool]:
        li = kougeki.maai_list(delivery, hoyuusya)
        print("li", li)
        for i, v in enumerate(li[::-1]):
            print("i, v", i, v)
            if i == 0 or not v:
                continue
            li[-i] = True
            break
        return li
    taiounized.taiouble = nega_dic
    taiounized.maai_list = maai_list
    return taiounized

_cfs_n_6_1 = AttackCorrection(name="鐘鳴らし：+2/+1", cond=mine_cf, taiounize=lambda c, d, h: papl_attack(c, d, h, 2, 1))
_cfs_n_6_2 = AttackCorrection(name="鐘鳴らし：対応不可、拡大遠1", cond=mine_cf, taiounize=_taiounize_cfs_n_6_2)

def _kouka_n_6_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).lingerings.append(_cfs_n_6_1)

def _kouka_n_6_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).lingerings.append(_cfs_n_6_2)

_choice_n_6_1 = TempKoudou("火力強化", auto_di, kouka=_kouka_n_6_1, todo=[["＋２／＋１"]])
_choice_n_6_2 = TempKoudou("射程延伸", auto_di, kouka=_kouka_n_6_2, todo=[["対応不可", "距離拡大(遠１)"]])

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(choice_layer(cards=[_choice_n_6_1, _choice_n_6_2], delivery=delivery, hoyuusya=hoyuusya))

n_6 = Card(megami=MG_HAGANE, img=img_card("o_n_6_s8"), name="鐘鳴らし", cond=ensin, type=CT_KOUDOU,
    kouka=_kouka_n_6)

_cfs_n_7 = ScalarCorrection(name="引力場", cond=auto_diic, scalar=SC_TATUZIN, value=-1)
_tenkaizi_n_7 = TempKoudou("引力場", auto_di, yazirusi=Yazirusi(from_code=UC_MAAI, to_mine=True, to_code=UC_AURA))
_tenkaizi_n_7_zenryoku = TempKoudou("引力場：全力化", auto_di, yazirusi=
    Yazirusi(from_code=UC_MAAI, to_mine=True, to_code=UC_AURA, kazu=2))

_n_7_zenryoku = Card(megami=MG_HAGANE, img=img_card("o_n_7_s7_2"), name="引力場：全力化", cond=auto_di, type=CT_HUYO,
    osame=int_di(2), tenkaizi=_tenkaizi_n_7_zenryoku, cfs=[_cfs_n_7], zenryoku=True)

n_7 = Card(megami=MG_HAGANE, img=img_card("o_n_7_s7_2"), name="引力場", cond=auto_di, type=CT_HUYO,
    osame=int_di(2), tenkaizi=_tenkaizi_n_7_zenryoku, cfs=[_cfs_n_7], zenryokuize=True, zenryokued=_n_7_zenryoku)
