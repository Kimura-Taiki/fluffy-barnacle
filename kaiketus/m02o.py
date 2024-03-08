#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import MG_YURINA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_ZENRYOKU,\
    CT_TAIOU, UC_LIFE, IMG_BYTE, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, TG_1_OR_MORE_DAMAGE,\
    UC_AURA
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.coous.attack_correction import Attack, AttackCorrection, mine_cf, BoolDIIC, auto_diic
from mod.delivery import Delivery
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_attack, papl_kougeki
from mod.coous.saiki import saiki_trigger
