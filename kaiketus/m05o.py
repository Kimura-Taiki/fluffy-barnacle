#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import enforce, opponent, MG_OBORO, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TG_END_PHASE,\
    SC_SMOKE, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI, BoolDIC, nega_dic
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
            lower=delivery.taba_target(hoyuusya, False, TC_TEHUDA), code=POP_ACT1)),
        POP_ACT1: lambda l, s: _sutecard_n_2(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

_after_n_2 = TempKoudou("影菱：攻撃後", cond=_cond_n_2, kouka=_kouka_n_2)

n_2 = Card(megami=MG_OBORO, img=img_card("o_n_2_s2"), name="影菱", cond=auto_di, type=CT_KOUGEKI,
    aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(2, 2), taiouble=nega_dic,
    after=_after_n_2, setti=True)