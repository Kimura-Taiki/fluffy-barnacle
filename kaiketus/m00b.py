#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_AURA,\
    UC_FLAIR, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_DIV, TC_KIRIHUDA, enforce,\
    USAGE_UNUSED, TG_2_OR_MORE_DAMAGE, USAGE_USED, MG_HONOKA
from mod.card.card import Card, auto_di, int_di, dima_di, nega_dic
from mod.card.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import choice_layer
from mod.coous.attack_correction import AttackCorrection, mine_cf, auto_diic, Attack
from mod.popup_message import popup_message
from mod.coous.saiki import saiki_trigger
from mod.card.kw.papl import papl_attack
from mod.card.kw.step import each_step
from mod.card.kw.syuutyuu import syuutyuu
from mod.card.kw.yazirusi import Yazirusi
from mod.card.kw.handraw import handraw

n_1 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_1.png"), name="花弁刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(0), aura_bar=auto_di, life_damage_func=int_di(1), maai_list=dima_di(4, 5))

n_2 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_2.png"), name="桜刀", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(3, 4))

n_3 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_3.png"), name="瞬霊式", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(5, 5), taiouble=nega_dic)

def _cond_n_4(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.b_params.during_taiou

_aan4 = TempKoudou(name="返し斬り：攻撃後", cond=_cond_n_4, yazirusi=Yazirusi(to_mine=True, to_code=UC_AURA))

n_4 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_4.png"), name="返し斬り", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(3, 4), after=_aan4, taiou=True)

def _kouka_n_5(delivery: Delivery, hoyuusya: int) -> None:
    syuutyuu(delivery=delivery, hoyuusya=hoyuusya)
    each_step(delivery=delivery, hoyuusya=hoyuusya)

n_5 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_5.png"), name="歩法", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_5)

n_6 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_6.png"), name="桜寄せ", cond=auto_di, type=CT_KOUDOU,
           kouka=Yazirusi(from_mine=False, from_code=UC_AURA, to_mine=True, to_code=UC_AURA).send, taiou=True)

def _kouka_n_7(delivery: Delivery, hoyuusya: int) -> None:
    Yazirusi(to_mine=True, to_code=UC_AURA, kazu=2).send(delivery=delivery, hoyuusya=hoyuusya)
    Yazirusi(to_mine=True, to_code=UC_FLAIR).send(delivery=delivery, hoyuusya=hoyuusya)

n_7 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_7.png"), name="光輝収束", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_n_7, zenryoku=True)

def _aura_damage_7(delivery: Delivery, hoyuusya: int) -> int:
    return delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_FLAIR)

n_8 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_8.png"), name="光の刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=_aura_damage_7, life_damage_func=int_di(1), maai_list=dima_di(3, 5))

_cfs_n_9 = AttackCorrection(name="精霊連携", cond=mine_cf, taiounize=lambda c, d, h: papl_attack(c, d, h, 1, 0))

n_9 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_n_9.png"), name="精霊連携", cond=auto_di, type=CT_HUYO,
           osame=int_di(3), cfs=[_cfs_n_9], zenryoku=True)

s_1 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_s_1.png"), name="光満ちる一刀", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(3), maai_list=dima_di(3, 4), kirihuda=True, flair=int_di(5))

s_2 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_s_2.png"), name="花吹雪の景色", cond=auto_di, type=CT_KOUDOU,
           kouka=Yazirusi(from_mine=False, from_code=UC_AURA, to_code=UC_MAAI, kazu=2).send, kirihuda=True, flair=int_di(4))

def _taiounize_s_3(kougeki: Card, delivery: Delivery, hoyuusya: int) -> Card:
    taiounized = copy(kougeki)
    if not taiounized.kirihuda:
        taiounized.aura_bar = auto_di
        taiounized.life_bar = auto_di
        taiounized.after = None
    return taiounized

s_3 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_s_3.png"), name="精霊たちの風", cond=auto_di, type=CT_KOUDOU,
           kouka=handraw, taiou=True, taiounize=_taiounize_s_3, kirihuda=True, flair=int_di(3))

_cfs_s_4 = saiki_trigger(cls=Card, file_name="cards/na_00_hajimari_b_s_4.png",
            name="煌めきの乱舞", cond=auto_diic, trigger=TG_2_OR_MORE_DAMAGE)

s_4 = Card(megami=MG_HONOKA, img=pygame.image.load("cards/na_00_hajimari_b_s_4.png"), name=
    "煌めきの乱舞", cond=auto_di, type=CT_KOUGEKI, aura_damage_func=int_di(2),
    life_damage_func=int_di(2), maai_list=dima_di(3, 5), kirihuda=True, flair=
    int_di(2), used=[_cfs_s_4])
