#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy
import random

from mod.const import enforce, opponent, MG_TIKAGE, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_KAIHEI, IMG_NO_CHOICE,\
    UC_AURA, UC_FLAIR, UC_DUST, SC_TATUZIN, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, TG_END_PHASE,\
    SC_TIKANDOKU, TC_MISIYOU, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, OBAL_USE_CARD,\
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

_ADDRESS = "na_09_chikage"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def _kaiki(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_huda_to_ryouiki(
        huda=enforce(enforce(moderator.last_layer(), PipelineLayer).huda, Huda).base,
        is_mine=False, taba_code=TC_MISIYOU)

_cond_p_1: BoolDI = lambda delivery, hoyuusya: not delivery.m_params(hoyuusya).played_standard

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

_hakizi_p_3 = TempKoudou("弛緩毒：破棄時", auto_di, kouka=_kaiki)

p_3 = Card(megami=MG_TIKAGE, img=img_card("o_p_3"), name="弛緩毒", cond=auto_di, type=CT_HUYO,
    osame=int_di(3), hakizi=_hakizi_p_3, cfs=[_cfs_p_3])

p_4 = Card(megami=MG_TIKAGE, img=img_card("o_p_4"), name="滅灯毒", cond=auto_di, type=CT_KOUDOU,
    kouka=Yazirusi(from_mine=True, from_code=UC_AURA, kazu=3).send,
    doku=True, unhuseable=True)
