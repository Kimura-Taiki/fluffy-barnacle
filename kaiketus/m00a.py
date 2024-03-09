#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_ISYUKU,\
    UC_AURA, CT_KOUGEKI, CT_KOUDOU, enforce, TC_TEHUDA, TC_SUTEHUDA,\
    TG_END_PHASE, MG_UTURO
from mod.classes import Card, Taba, Delivery, moderator
from mod.card.card import auto_di, int_di, dima_di
from mod.card.temp_koudou import TempKoudou
from mod.ol.choice import choice_layer
from mod.coous.continuous import BoolDIIC, mine_cf
from mod.coous.saiki import saiki_trigger
from mod.card.kw.suki import suki_card
from mod.card.kw.papl import papl_kougeki
from mod.card.kw.step import each_step
from mod.card.kw.yazirusi import Yazirusi, ya_moguri
from mod.card.kw.syuutyuu import syuutyuu, isyuku, reduce_syuutyuu

n_1 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_1.png"), name="投射", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(3), life_damage_func=int_di(1), maai_list=dima_di(5, 9))

n_2 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_2.png"), name="脇斬り", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(2), life_damage_func=int_di(2), maai_list=dima_di(2, 3))

n_3 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_3.png"), name="牽制", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(2), life_damage_func=int_di(1), maai_list=dima_di(1, 3))

n_4 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_4.png"), name="背中刺し", cond=auto_di, type=CT_KOUGEKI,
              aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(1, 1))

n_5 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_5.png"), name="二刀一閃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(2), maai_list=dima_di(2, 3), zenryoku=True)

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    syuutyuu(delivery=delivery, hoyuusya=hoyuusya)
    each_step(delivery=delivery, hoyuusya=hoyuusya)

n_6 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_6.png"), name="歩法", cond=auto_di, type=CT_KOUDOU, kouka=_kouka_n_6)

n_7 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_7.png"), name="潜り", cond=auto_di, type=CT_KOUDOU,
           kouka=ya_moguri.send, taiou=True)

n_8 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_8.png"), name="患い", cond=auto_di, type=CT_KOUDOU,
           kouka=isyuku, taiou=True, taiounize=lambda c, d, h: papl_kougeki(c, d, h, -1, 0))

_atk_n_9 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_9.png"), name="陰の罠：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
                aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list=dima_di(2, 3))

n_9 = suki_card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_9.png"), name="陰の罠", cond=auto_di,
                osame=int_di(2), hakizi=_atk_n_9)

s_1 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_s_1.png"), name="数多ノ刃", cond=auto_di, type=CT_KOUGEKI,
           aura_damage_func=int_di(4), life_damage_func=int_di(3), maai_list=dima_di(1, 2), kirihuda=True, flair=int_di(5))

def _kouka_s_2(delivery: Delivery, hoyuusya: int) -> None:
    for _ in range(2):
        delivery.hand_draw(hoyuusya=hoyuusya, is_mine=True)

s_2 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_s_2.png"), name="闇凪ノ声", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_2, kirihuda=True, flair=int_di(4))

s_3 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_s_3.png"), name="苦ノ外套", cond=auto_di, type=CT_KOUDOU,
           kouka=Yazirusi(from_code=UC_AURA, kazu=2).send, taiou=True, taiounize=lambda c, d, h: papl_kougeki(c, d, h, -2, 0), kirihuda=True, flair=int_di(3))

_cond_s_4: BoolDIIC = lambda delivery, call_h, cf_h, card: mine_cf(delivery, call_h, cf_h, card) and\
    delivery.ouka_count(hoyuusya=cf_h, is_mine=False, utuwa_code=UC_DUST) >= 10

_cfs_s_4 = saiki_trigger(cls=Card, file_name="cards/na_00_hajimari_a_s_4.png",
            name="奪イノ茨", cond=_cond_s_4, trigger=TG_END_PHASE)

def _kouka_s_4(delivery: Delivery, hoyuusya: int) -> None:
    for huda in list(enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=TC_TEHUDA), Taba)):
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_SUTEHUDA)
    reduce_syuutyuu(delivery=delivery, hoyuusya=hoyuusya)

s_4 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_s_4.png"), name="奪イノ茨", cond=auto_di, type=CT_KOUDOU,
           kouka=_kouka_s_4, zenryoku=True, kirihuda=True, flair=int_di(1), cfs=[_cfs_s_4])
