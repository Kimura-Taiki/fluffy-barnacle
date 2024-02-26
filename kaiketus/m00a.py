#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_ISYUKU, UC_AURA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO,\
    enforce, TC_TEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, USAGE_USED, USAGE_UNUSED, TG_END_PHASE
from mod.card.card import Card, auto_di, int_di, dima_di
from mod.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import choice_layer
from mod.taba import Taba
from mod.coous.trigger import Trigger, BoolDII, auto_dii, mine_cf
from mod.popup_message import popup_message

n_1 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_1.png"), name="投射", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(5, 9))

n_2 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_2.png"), name="脇斬り", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(2, 3))

n_3 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_3.png"), name="牽制", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(1, 3))

n_4 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_4.png"), name="背中刺し", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(1, 1))

n_5 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_5.png"), name="二刀一閃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(2), maai_list=dima_di(2, 3), zenryoku=True)

def _kouka_n_6_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_DUST, kazu=1)

def _kouka_n_6_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI, kazu=1)

tkn61 = TempKoudou(name="歩法：潜り", cond=auto_di, kouka=_kouka_n_6_1, todo=[[False, UC_MAAI, False, UC_DUST, 1]])
tkn62 = TempKoudou(name="歩法：離脱", cond=auto_di, kouka=_kouka_n_6_2, todo=[[False, UC_DUST, False, UC_MAAI, 1]])

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    moderator.append(over_layer=choice_layer(cards=[tkn61, tkn62], delivery=delivery, hoyuusya=hoyuusya))

n_6 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_6.png"), name="歩法", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_6)

def _kouka_n_7(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=True, to_code=UC_DUST, kazu=1)

n_7 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_7.png"), name="潜り", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_n_7, taiou=True)

def _kouka_n_8(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=False, to_code=UC_ISYUKU, kazu=1)

def _taiounize_n_8(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)-1
    taiounized.aura_damage_func = aura_damage_func
    return taiounized

n_8 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_8.png"), name="患い", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_n_8, taiou=True, taiounize=_taiounize_n_8)

_atk_n_9 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_9.png"), name="陰の罠：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
                aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(2, 3))

n_9 = Card(img=pygame.image.load("cards/na_00_hajimari_a_n_9.png"), name="陰の罠", cond=auto_di, type=CT_HUYO,
           osame=int_di(2), suki=auto_di, hakizi=_atk_n_9)

s_1 = Card(img=pygame.image.load("cards/na_00_hajimari_a_s_1.png"), name="数多ノ刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(3), maai_list=dima_di(1, 2), kirihuda=True, flair=int_di(5))

def _kouka_s_2(delivery: Delivery, hoyuusya: int) -> None:
    for _ in range(2):
        delivery.hand_draw(hoyuusya=hoyuusya, is_mine=True)

s_2 = Card(img=pygame.image.load("cards/na_00_hajimari_a_s_2.png"), name="闇凪ノ声", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_2, kirihuda=True, flair=int_di(4))

def _kouka_s_3(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_AURA, to_mine=False, to_code=UC_DUST, kazu=2)

def _taiounize_s_3(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)-2
    taiounized.aura_damage_func = aura_damage_func
    return taiounized

s_3 = Card(img=pygame.image.load("cards/na_00_hajimari_a_s_3.png"), name="苦ノ外套", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_3, taiou=True, taiounize=_taiounize_s_3, kirihuda=True, flair=int_di(3))

def _s_s_4(delivery: Delivery, hoyuusya: int) -> None:
    if not (huda := next((huda for huda in enforce(
    delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA),
    Taba) if huda.card.name == "奪イノ茨"), None)):
        popup_message.add(f"切り札「奪イノ茨」が見つかりませんでした")
        return
    if huda.usage != USAGE_USED:
        return
    huda.usage = USAGE_UNUSED
    popup_message.add(f"切り札「奪イノ茨」が再起しました")

_saiki_s_4 = Card(img=pygame.image.load("cards/na_00_hajimari_a_s_4.png"), name="即再起：奪イノ茨", cond=auto_di, type=CT_KOUDOU,
                  kouka=_s_s_4)

_cond_s_4: BoolDII = lambda delivery, call_h, cf_h: mine_cf(delivery, call_h, cf_h) and\
    delivery.ouka_count(hoyuusya=cf_h, is_mine=False, utuwa_code=UC_DUST) >= 10

_cfs_s_4 = Trigger(name="奪イノ茨", cond=_cond_s_4, trigger=TG_END_PHASE, effect=_saiki_s_4)

def _kouka_s_4(delivery: Delivery, hoyuusya: int) -> None:
    for huda in list(enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=TC_TEHUDA), Taba)):
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_SUTEHUDA)
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_SYUUTYUU, to_mine=False, to_code=UC_ZYOGAI, kazu=2)

s_4 = Card(img=pygame.image.load("cards/na_00_hajimari_a_s_4.png"), name="奪イノ茨", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_4, zenryoku=True, kirihuda=True, flair=int_di(1), cfs=[_cfs_s_4])
