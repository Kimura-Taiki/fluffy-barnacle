#                 20                  40                  60                 79
from copy import copy

from mod.const import enforce
from mod.classes import Card, Delivery
from mod.coous.attack_correction import Attack

def papl_kougeki(card: Card, delivery: Delivery, hoyuusya: int, aura: int,
                 life: int) -> Card:
    taiounized = copy(card)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return card.aura_damage_func(delivery, hoyuusya)+aura
    def life_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return card.life_damage_func(delivery, hoyuusya)+life
    taiounized.aura_damage_func = aura_damage_func
    taiounized.life_damage_func = life_damage_func
    return taiounized

def papl_attack(card: Attack, delivery: Delivery, hoyuusya: int, aura: int,
                 life: int) -> Attack:
    taiounized = copy(card)
    def aura_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return card.aura_damage_func(delivery, hoyuusya)+aura
    def life_damage_func(delivery: Delivery, hoyuusya: int) -> int:
        return card.life_damage_func(delivery, hoyuusya)+life
    taiounized.aura_damage_func = aura_damage_func
    taiounized.life_damage_func = life_damage_func
    return taiounized
