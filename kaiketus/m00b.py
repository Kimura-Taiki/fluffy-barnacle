#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_AURA,\
    UC_FLAIR, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, TC_KIRIHUDA, enforce,\
    USAGE_UNUSED, TG_2_OR_MORE_DAMAGE, USAGE_USED
from mod.card.card import Card, auto_di, int_di, dima_di, nega_dic
from mod.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import choice_layer
from mod.coous.attack_correction import AttackCorrection, BoolDII, mine_cf, Attack
from mod.coous.trigger import Trigger, auto_dii
from mod.taba import Taba
from mod.popup_message import popup_message

n_1 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_1.png"), name="花弁刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(0), aura_bar=auto_di, life_damage_func=int_di(1), maai_list=dima_di(4, 5))

n_2 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_2.png"), name="桜刀", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

n_3 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_3.png"), name="瞬霊式", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(5, 5), taiouble=nega_dic)

def _kouka_n_4(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_AURA, kazu=1)

def _cond_n_4(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.b_params.during_taiou

_aan4 = TempKoudou(name="返し斬り：攻撃後", cond=_cond_n_4, kouka=_kouka_n_4, todo=[[False, UC_DUST, True, UC_AURA, 1]])

n_4 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_4.png"), name="返し斬り", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(3, 4), after=_aan4, taiou=True)

def _kouka_n_5_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_DUST, kazu=1)

def _kouka_n_5_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI, kazu=1)

tkn51 = TempKoudou(name="歩法：潜り", cond=auto_di, kouka=_kouka_n_5_1, todo=[[False, UC_MAAI, False, UC_DUST, 1]])
tkn52 = TempKoudou(name="歩法：離脱", cond=auto_di, kouka=_kouka_n_5_2, todo=[[False, UC_DUST, False, UC_MAAI, 1]])

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    moderator.append(over_layer=choice_layer(cards=[tkn51, tkn52], delivery=delivery, hoyuusya=hoyuusya))

n_5 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_5.png"), name="歩法", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_5)

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_AURA, to_mine=True, to_code=UC_AURA, kazu=1)

n_6 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_6.png"), name="桜寄せ", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_n_6, taiou=True)

def _kouka_n_7(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_AURA, kazu=2)
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_FLAIR, kazu=1)

n_7 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_7.png"), name="光輝収束", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_n_7, zenryoku=True)

def _aura_damage_7(delivery: Delivery, hoyuusya: int) -> int:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_FLAIR)

n_8 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_8.png"), name="光の刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=_aura_damage_7, life_damage_func=int_di(1), maai_list=dima_di(3, 5))

def _taiounize_cfs_n_9(kougeki: Attack, delivery: Delivery, hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)+1
    taiounized.aura_damage_func = aura_damage_func
    return taiounized

_cfs_n_9 = AttackCorrection(name="精霊連携", cond=mine_cf, taiounize=_taiounize_cfs_n_9)

n_9 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_9.png"), name="精霊連携", cond=auto_di, type=CT_HUYO,
           osame=int_di(3), cfs=[_cfs_n_9], zenryoku=True)

s_1 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_1.png"), name="光満ちる一刀", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(3), maai_list=dima_di(3, 4), kirihuda=True, flair=int_di(5))

def _kouka_s_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_AURA, to_mine=False, to_code=UC_MAAI, kazu=2)

s_2 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_2.png"), name="花吹雪の景色", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_2, kirihuda=True, flair=int_di(4))

def _kouka_s_3(delivery: Delivery, hoyuusya: int) -> None:
    delivery.hand_draw(hoyuusya=hoyuusya, is_mine=True)

def _taiounize_s_3(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    if not taiounized.kirihuda:
        taiounized.aura_bar = auto_di
        taiounized.life_bar = auto_di
        taiounized.after = None
    return taiounized

s_3 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_3.png"), name="精霊たちの風", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_3, taiou=True, taiounize=_taiounize_s_3, kirihuda=True, flair=int_di(3))

from kaiketus.temp import saiki_kouka, saiki_card

# _saiki_s_4 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_4.png"), name="即再起：煌めきの乱舞", cond=auto_di, type=CT_KOUDOU,
#                   kouka=saiki_kouka(card_name="煌めきの乱舞"))
_saiki_s_4 = enforce(saiki_card(cls=Card, file_name="cards/na_00_hajimari_b_s_4.png", name="煌めきの乱舞"), Card)

_cfs_s_4 = Trigger(name="煌めきの乱舞", cond=auto_dii, trigger=TG_2_OR_MORE_DAMAGE, effect=_saiki_s_4)

#                 20                  40                  60                 79
s_4 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_4.png"), name=
    "煌めきの乱舞", cond=auto_di, type=CT_KOUGEKI, aura_damage_func=int_di(2),
    life_damage_func=int_di(2), maai_list=dima_di(3, 5), kirihuda=True, flair=
    int_di(2), cfs=[_cfs_s_4])
