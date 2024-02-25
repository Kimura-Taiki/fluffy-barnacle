from typing import Callable
from functools import partial

from mod.const import WX, WY, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, side_name, enforce, POP_RECEIVED
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory
from mod.huda.huda import Huda
from mod.taba import Taba
from mod.card.card import Card
from mod.card.damage import Damage
from mod.popup_message import popup_message
from mod.tf.taba_factory import TabaFactory

HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
_0DAMAGE = Damage(img=IMG_AURA_DAMAGE, name="打ち消しました", dmg=0, from_code=UC_AURA, to_code=UC_DUST)

def uke_taba(kougeki: Card, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> Taba:
    mouseup = partial(_uke_mouseup, kougeki=kougeki, discard_source=discard_source, delivery=delivery, hoyuusya=hoyuusya)
    factory = _uke_factory(mouse_up=mouseup)
    return factory.maid_by_cards(cards=(_uke_cards(card=kougeki, delivery=delivery, hoyuusya=hoyuusya)), hoyuusya=hoyuusya)

def _uke_cards(card: Card, delivery: Delivery, hoyuusya: int) -> list[Card]:
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
    return Damage(img=IMG_AURA_DAMAGE, name="オーラで受けました", dmg=dmg, from_code=UC_AURA, to_code=UC_DUST)

def _ld_card(dmg: int) -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="オーラで受けました", dmg=dmg, from_code=UC_LIFE, to_code=UC_FLAIR)

def _uke_factory(mouse_up: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={"mouseup": mouse_up}, huda_y=HAND_Y, is_ol=True)

def _uke_mouseup(huda: Huda, kougeki: Card, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(f"{side_name(hoyuusya)}の「{kougeki.name}」を{huda.card.name}")
    huda.card.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_RECEIVED)
    # discard_source()

