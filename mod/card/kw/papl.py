#                 20                  40                  60                 79
from copy import copy

from mod.classes import Delivery
from mod.coous.attack_correction import Attack

def papl(kougeki: Attack, aura: int, life: int, delivery: Delivery,
         hoyuusya: int) -> Attack:
    taiounized = copy(kougeki)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.aura_damage_func(delivery, hoyuusya)+aura
    def life_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return kougeki.life_damage_func(delivery, hoyuusya)+life
    taiounized.aura_damage_func = aura_damage_func
    taiounized.life_damage_func = life_damage_func
    return taiounized
