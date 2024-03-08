#                 20                  40                  60                 79
import pygame
from pygame import Surface
from copy import copy

from mod.const import UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, UC_DUST
from mod.classes import Delivery, moderator
from mod.card.card import auto_di
from mod.card.temp_koudou import TempKoudou
from mod.ol.choice import choice_layer

def _kouka_moguri(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_DUST, kazu=1)

def _kouka_ridatu(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI, kazu=1)

tk_moguri = TempKoudou(name="潜り", cond=auto_di, kouka=_kouka_moguri, todo=[[False, UC_MAAI, False, UC_DUST, 1]])
tk_ridatu = TempKoudou(name="離脱", cond=auto_di, kouka=_kouka_ridatu, todo=[[False, UC_DUST, False, UC_MAAI, 1]])

def each_step(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    moderator.append(over_layer=choice_layer(cards=[tk_moguri, tk_ridatu], delivery=delivery, hoyuusya=hoyuusya))
