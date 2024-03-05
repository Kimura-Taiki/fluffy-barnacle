#                 20                  40                  60                 79
from mod.const import IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, UC_AURA, UC_DUST,\
    UC_LIFE, UC_FLAIR
from mod.classes import Card, Delivery
from mod.card.damage import Damage

_0DAMAGE = Damage(img=IMG_AURA_DAMAGE, name="打ち消しました", dmg=0,
                  from_code=UC_AURA, to_code=UC_DUST)

def uke_cards(card: Card, delivery: Delivery, hoyuusya: int) -> list[Card]:
    aura_damage = card.aura_damage(delivery=delivery, hoyuusya=hoyuusya)
    life_damage = card.life_damage(delivery=delivery, hoyuusya=hoyuusya)
    if aura_damage is None:
        return [_0DAMAGE] if life_damage is None else [_ld_card(dmg=life_damage)]
    else:
        ad_card = _ad_card(dmg=aura_damage)
        if life_damage is None:
            return [ad_card]
        else:
            ld_card = _ld_card(dmg=life_damage)
            is_receivable = ad_card.can_damage(delivery=delivery, hoyuusya=hoyuusya)
            return [ad_card, ld_card] if is_receivable else [ld_card]

def _ad_card(dmg: int) -> Damage:
    return Damage(img=IMG_AURA_DAMAGE, name="オーラで防ぎました", dmg=dmg, from_code=UC_AURA, to_code=UC_DUST)

def _ld_card(dmg: int) -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="ライフで受けました", dmg=dmg, from_code=UC_LIFE, to_code=UC_FLAIR)
