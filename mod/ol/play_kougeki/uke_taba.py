from typing import Callable
from functools import partial

from mod.const import WX, WY, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, side_name
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory
from mod.huda import Huda
from mod.taba import Taba
from mod.card import Damage, Card
from mod.popup_message import popup_message
from mod.tf.taba_factory import TabaFactory

HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150

def uke_taba(kougeki: Card, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> Taba:
    mouseup = partial(_uke_mouseup, kougeki=kougeki, discard_source=discard_source, delivery=delivery, hoyuusya=hoyuusya)
    factory = _uke_factory(mouse_up=mouseup)
    return factory.maid_by_cards(cards=(_uke_cards(card=kougeki, delivery=delivery, hoyuusya=hoyuusya)), hoyuusya=hoyuusya)

def _uke_cards(card: Card, delivery: Delivery, hoyuusya: int) -> list[Card]:
    ad_card = Damage(img=IMG_AURA_DAMAGE, name="オーラで受けました", dmg=card.aura_damage(
        delivery, hoyuusya), from_code=UC_AURA, to_code=UC_DUST)
    ld_card = Damage(img=IMG_LIFE_DAMAGE, name="ライフに通しました", dmg=card.life_damage(
        delivery, hoyuusya), from_code=UC_LIFE, to_code=UC_FLAIR)
    can_receive_aura = ad_card.can_damage(delivery=delivery, hoyuusya=hoyuusya)
    return [ad_card, ld_card] if can_receive_aura and not card.aura_bar(delivery, hoyuusya) else [ld_card]

def _uke_factory(mouse_up: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={"mouseup": mouse_up}, huda_y=HAND_Y, is_ol=True)

def _uke_mouseup(huda: Huda, kougeki: Card, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> None:
    huda.card.kaiketu(delivery=delivery, hoyuusya=hoyuusya)
    popup_message.add(f"{side_name(hoyuusya)}の「{kougeki.name}」を{huda.card.name}")
    discard_source()
