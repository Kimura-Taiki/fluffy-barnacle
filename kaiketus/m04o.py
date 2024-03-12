#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import enforce, opponent, MG_TOKOYO, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA, UC_DUST, SC_TATUZIN, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TG_END_PHASE,\
    SC_SMOKE, TC_YAMAHUDA, TC_TEHUDA
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di, BoolDI, SuuziDI, BoolDIC
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
