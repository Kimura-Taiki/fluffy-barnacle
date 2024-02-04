import pygame

from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_MAAI, UC_DUST
from mod.card import Kougeki, Koudou, auto_di, int_di, dima_di, KoukaDI
from mod.temp_koudou import TempKoudou
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.ol.choice import Choice

n_1 = Kougeki(img=pygame.image.load("cards/na_00_hajimari_a_n_1.png"), name="投射", cond=auto_di,
              aura_damage=int_di(3), life_damage=int_di(1), maai_list=dima_di(5, 9))

n_2 = Kougeki(img=pygame.image.load("cards/na_00_hajimari_a_n_2.png"), name="脇斬り", cond=auto_di,
              aura_damage=int_di(2), life_damage=int_di(2), maai_list=dima_di(2, 3))

n_3 = Kougeki(img=pygame.image.load("cards/na_00_hajimari_a_n_3.png"), name="牽制", cond=auto_di,
              aura_damage=int_di(2), life_damage=int_di(1), maai_list=dima_di(1, 3))

n_4 = Kougeki(img=pygame.image.load("cards/na_00_hajimari_a_n_4.png"), name="背中刺し", cond=auto_di,
              aura_damage=int_di(3), life_damage=int_di(2), maai_list=dima_di(1, 1))

def _kouka_n_6_1(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_MAAI, to_mine=False, to_code=UC_DUST, kazu=1)

def _kouka_n_6_2(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI, kazu=1)

tkn61 = TempKoudou(name="潜り", cond=auto_di, kouka=_kouka_n_6_1, todo=[[False, UC_MAAI, False, UC_DUST, 1]])
tkn62 = TempKoudou(name="離脱", cond=auto_di, kouka=_kouka_n_6_2, todo=[[False, UC_DUST, False, UC_MAAI, 1]])

def _kouka_n_6(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)
    moderator.append(over_layer=Choice(cards=[tkn61, tkn62], delivery=delivery, hoyuusya=hoyuusya))

n_6 = Koudou(img=pygame.image.load("cards/na_00_hajimari_a_n_6.png"), name="歩法", cond=auto_di, kouka=_kouka_n_6)

# n_7 = Koudou(img=pygame.image.load("cards/na_00_hajimari_a_n_7.png"), name="潜り", cond=auto_di,
#              aura_damage=int_di(3), life_damage=int_di(2), maai_list=dima_di(1, 1))

# n_8 = Koudou(img=pygame.image.load("cards/na_00_hajimari_a_n_8.png"), name="患い", cond=auto_di,
#              aura_damage=int_di(3), life_damage=int_di(2), maai_list=dima_di(1, 1))
