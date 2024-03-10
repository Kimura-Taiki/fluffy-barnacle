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

_ADDRESS = "na_03_himika"
def img_card(add: str) ->  Surface:
    return pygame.image.load(f"cards/{_ADDRESS}_{add}.png")

def renka(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.m_params(hoyuusya=hoyuusya).use_card_count >= 2

