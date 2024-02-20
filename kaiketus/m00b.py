import pygame
from copy import copy
from functools import partial

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST, UC_ISYUKU, UC_AURA, CT_KOUGEKI, CT_KOUDOU, CT_HUYO,\
    enforce, TC_TEHUDA, TC_SUTEHUDA
from mod.card import Card, auto_di, int_di, dima_di
from mod.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import choice_layer
from mod.taba import Taba

n_1 = Card(img=pygame.image.load("cards/na_00_hajimari_b_n_1.png"), name="花弁刃", cond=auto_di, type=CT_KOUGEKI,
              aura_damage=int_di(0), aura_bar=auto_di, life_damage=int_di(1), maai_list=dima_di(4, 5))
